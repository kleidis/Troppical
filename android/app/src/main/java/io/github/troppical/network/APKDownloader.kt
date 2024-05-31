package io.github.troppical.network

import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.ResponseBody
import java.io.File
import java.io.FileOutputStream
import java.io.IOException

class APKDownloader(private val url: String, private val outputFile: File) {

    fun download(onComplete: (Boolean) -> Unit) {
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
                        try {
                            val inputStream = body.byteStream()
                            val outputStream = FileOutputStream(outputFile)
                            val buffer = ByteArray(4096)
                            var bytesRead: Int
                            while (inputStream.read(buffer).also { bytesRead = it } != -1) {
                                outputStream.write(buffer, 0, bytesRead)
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
