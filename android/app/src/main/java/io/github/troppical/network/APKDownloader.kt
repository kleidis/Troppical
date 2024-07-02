package io.github.troppical.network

import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.ResponseBody
import org.chromium.net.CronetEngine
import com.google.net.cronet.okhttp.CronetCallFactory
import java.io.File
import java.io.FileOutputStream
import java.io.IOException

class APKDownloader(private val url: String, private val outputFile: File) {

    private var useCronet: Boolean = false

    fun setUseCronet(enable: Boolean) {
        useCronet = enable
    }

    private fun getClient(): OkHttpClient {
        return if (useCronet) {
            val cronetEngine = CronetEngine.Builder(context)
                .build()
            val callFactory = CronetCallFactory.newBuilder(cronetEngine).build()

            OkHttpClient.Builder()
                .callFactory(callFactory)
                .build()
        } else {
            OkHttpClient()
        }
    }

    fun download(onProgress: (Int) -> Unit, onComplete: (Boolean) -> Unit) {
        val client = getClient()
        val request = Request.Builder().url(url).build()

        client.newCall(request).enqueue(object : okhttp3.Callback {
            override fun onFailure(call: okhttp3.Call, e: IOException) {
                e.printStackTrace()
                onComplete(false)
            }

            override fun onResponse(call: okhttp3.Call, response: okhttp3.Response) {
                if (response.isSuccessful) {
                    response.body?.let { body ->
                        val contentLength = body.contentLength()
                        try {
                            val inputStream = body.byteStream()
                            val outputStream = FileOutputStream(outputFile)
                            val buffer = ByteArray(4096)
                            var bytesRead: Int
                            var totalBytesRead: Long = 0

                            while (inputStream.read(buffer).also { bytesRead = it } != -1) {
                                outputStream.write(buffer, 0, bytesRead)
                                totalBytesRead += bytesRead
                                val progress = (totalBytesRead * 100 / contentLength).toInt()
                                onProgress(progress)
                            }
                            outputStream.flush()
                            outputStream.close()
                            inputStream.close()
                            onComplete(true)
                        } catch (e: IOException) {
                            e.printStackTrace()
                            onComplete(false)
                        }
                    } ?: run {
                        onComplete(false)
                    }
                } else {
                    onComplete(false)
                }
            }
        })
    }
}
