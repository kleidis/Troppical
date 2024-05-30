package io.github.troppical.network

import com.google.gson.Gson
import okhttp3.*
import java.io.IOException
import java.security.SecureRandom
import java.security.cert.CertificateException
import java.security.cert.X509Certificate
import java.util.concurrent.TimeUnit
import javax.net.ssl.*

class RequestNetworkController private constructor() {
    companion object {
        const val GET = "GET"
        const val POST = "POST"
        const val PUT = "PUT"
        const val DELETE = "DELETE"

        const val REQUEST_PARAM = 0
        const val REQUEST_BODY = 1

        private const val SOCKET_TIMEOUT = 15000
        private const val READ_TIMEOUT = 25000

        @Volatile
        private var mInstance: RequestNetworkController? = null

        @JvmStatic
        fun getInstance(): RequestNetworkController {
            return mInstance ?: synchronized(this) {
                mInstance ?: RequestNetworkController().also { mInstance = it }
            }
        }
    }

    private var client: OkHttpClient? = null

    private fun getClient(): OkHttpClient {
        if (client == null) {
            val builder = OkHttpClient.Builder()

            try {
                val trustAllCerts = arrayOf<TrustManager>(
                    object : X509TrustManager {
                        override fun checkClientTrusted(chain: Array<X509Certificate>, authType: String) {}
                        override fun checkServerTrusted(chain: Array<X509Certificate>, authType: String) {}
                        override fun getAcceptedIssuers(): Array<X509Certificate> = arrayOf()
                    }
                )

                val sslContext = SSLContext.getInstance("TLS").apply {
                    init(null, trustAllCerts, SecureRandom())
                }
                val sslSocketFactory = sslContext.socketFactory
                builder.sslSocketFactory(sslSocketFactory, trustAllCerts[0] as X509TrustManager)
                builder.connectTimeout(SOCKET_TIMEOUT.toLong(), TimeUnit.MILLISECONDS)
                builder.readTimeout(READ_TIMEOUT.toLong(), TimeUnit.MILLISECONDS)
                builder.writeTimeout(READ_TIMEOUT.toLong(), TimeUnit.MILLISECONDS)
                builder.hostnameVerifier { _: String?, _: SSLSession? -> true }
            } catch (e: Exception) {
                e.printStackTrace()
            }

            client = builder.build()
        }
        return client!!
    }

    fun execute(
        requestNetwork: RequestNetwork, method: String, url: String, tag: String,
        requestListener: RequestNetwork.RequestListener
    ) {
        val reqBuilder = Request.Builder()
        val headerBuilder = Headers.Builder()

        if (requestNetwork.headers.isNotEmpty()) {
            requestNetwork.headers.forEach { (key, value) ->
                headerBuilder.add(key, value.toString())
            }
        }

        try {
            if (requestNetwork.requestType == REQUEST_PARAM) {
                if (method == GET) {
                    val httpBuilder = HttpUrl.parse(url)?.newBuilder()
                        ?: throw NullPointerException("unexpected url: $url")

                    if (requestNetwork.params.isNotEmpty()) {
                        requestNetwork.params.forEach { (key, value) ->
                            httpBuilder.addQueryParameter(key, value.toString())
                        }
                    }

                    reqBuilder.url(httpBuilder.build()).headers(headerBuilder.build()).get()
                } else {
                    val formBuilder = FormBody.Builder()
                    if (requestNetwork.params.isNotEmpty()) {
                        requestNetwork.params.forEach { (key, value) ->
                            formBuilder.add(key, value.toString())
                        }
                    }

                    val reqBody = formBuilder.build()
                    reqBuilder.url(url).headers(headerBuilder.build()).method(method, reqBody)
                }
            } else {
                val reqBody = RequestBody.create(
                    MediaType.parse("application/json"),
                    Gson().toJson(requestNetwork.params)
                )

                if (method == GET) {
                    reqBuilder.url(url).headers(headerBuilder.build()).get()
                } else {
                    reqBuilder.url(url).headers(headerBuilder.build()).method(method, reqBody)
                }
            }

            val req = reqBuilder.build()

            getClient().newCall(req).enqueue(object : Callback {
                override fun onFailure(call: Call, e: IOException) {
                    requestNetwork.activity.runOnUiThread {
                        requestListener.onErrorResponse(tag, e.message ?: "Unknown error")
                    }
                }

                override fun onResponse(call: Call, response: Response) {
                    val responseBody = response.body()?.string()?.trim() ?: ""
                    requestNetwork.activity.runOnUiThread {
                        val responseHeaders = response.headers().toMap()
                        requestListener.onResponse(tag, responseBody, responseHeaders)
                    }
                }
            })
        } catch (e: Exception) {
            requestListener.onErrorResponse(tag, e.message ?: "Unknown error")
        }
    }
}
