package io.github.troppical.network

import android.content.Context
import com.google.android.gms.net.CronetProviderInstaller
import org.chromium.net.CronetEngine
import org.chromium.net.UrlRequest
import java.io.File
import java.io.FileOutputStream
import java.io.IOException
import java.util.concurrent.Executor
import java.util.concurrent.Executors

class APKDownloader(private val context: Context, private val url: String, private val outputFile: File) {

    private var useCronet: Boolean = false

    fun setUseCronet(enable: Boolean) {
        useCronet = enable
    }

    fun download(onProgress: (Int) -> Unit, onComplete: (Boolean) -> Unit) {
        if (useCronet) {
            downloadWithCronet(onProgress, onComplete)
        } else {
            downloadWithOkHttp(onProgress, onComplete)
        }
    }

    private fun downloadWithOkHttp(onProgress: (Int) -> Unit, onComplete: (Boolean) -> Unit) {
        val client = OkHttpClient()
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

    private fun downloadWithCronet(onProgress: (Int) -> Unit, onComplete: (Boolean) -> Unit) {
        val cronetEngine = CronetEngine.Builder(context)
            .build()
        val executor: Executor = Executors.newSingleThreadExecutor()

        val requestBuilder = cronetEngine.newUrlRequestBuilder(
            url,
            object : UrlRequest.Callback() {
                override fun onRedirectReceived(
                    request: UrlRequest?,
                    info: UrlRequest.RedirectInfo?
                ) {
                    // Handle redirect if necessary
                }

                override fun onResponseStarted(request: UrlRequest?, info: UrlRequest.ResponseInfo?) {
                    // Start receiving response
                }

                override fun onReadCompleted(
                    request: UrlRequest?,
                    info: UrlRequest.ResponseInfo?,
                    byteBuffer: java.nio.ByteBuffer?
                ) {
                    // Read and save the response
                    byteBuffer?.array()?.let { byteArray ->
                        try {
                            val outputStream = FileOutputStream(outputFile, true)
                            outputStream.write(byteArray)
                            outputStream.flush()
                            outputStream.close()

                            // Calculate progress
                            val totalBytesRead = info?.receivedByteCount ?: 0L
                            val progress = (totalBytesRead * 100 / info?.contentLength ?: 1L).toInt()
                            onProgress(progress)
                        } catch (e: IOException) {
                            e.printStackTrace()
                            onComplete(false)
                        }
                    }
                }

                override fun onSucceeded(request: UrlRequest?, info: UrlRequest.ResponseInfo?) {
                    onComplete(true)
                }

                override fun onFailed(request: UrlRequest?, info: UrlRequest.ResponseInfo?, error: java.io.IOException?) {
                    error?.printStackTrace()
                    onComplete(false)
                }
            },
            executor
        )

        requestBuilder.build().start()
    }
}
