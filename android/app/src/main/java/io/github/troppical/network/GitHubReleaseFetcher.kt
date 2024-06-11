package io.github.troppical.network

import android.content.Context
import android.view.View
import io.ktor.client.*
import io.ktor.client.call.*
import io.ktor.client.plugins.contentnegotiation.*
import io.ktor.client.request.*
import io.ktor.client.statement.*
import io.ktor.client.engine.cio.*
import io.ktor.serialization.kotlinx.json.*
import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable
import kotlinx.serialization.json.Json
import com.google.android.material.dialog.MaterialAlertDialogBuilder
import io.github.troppical.R
import java.io.IOException

@Serializable
data class GitHubRelease(
    val assets: List<Asset>,
    @SerialName("tag_name") val tagName: String,
    val prerelease: Boolean
)

@Serializable
data class Asset(
    val name: String,
    @SerialName("browser_download_url") val browserDownloadUrl: String
)

class GitHubReleaseFetcher(private val owner: String, private val repo: String, private val context: Context) {

    private val client = HttpClient(CIO) {
        install(ContentNegotiation) {
            json(Json { ignoreUnknownKeys = true })
        }
    }

    suspend fun fetchArtifactDirectLinkAndTag(artifactName: String): Pair<String?, String?> {
        val progressDialog = MaterialAlertDialogBuilder(context)
                .setTitle("Initializing")
                .setView(R.layout.progress_dialog)
                .setCancelable(false)
                .create()

        progressDialog.show()
        progressIndicator = progressDialog.findViewById(R.id.progress_indicator)!!
        val url = "https://api.github.com/repos/$owner/$repo/releases/latest"
        return try {
            val response: HttpResponse = client.get(url) {
                onDownload { bytesSentTotal, contentLength ->
                    if (contentLength != -1L) {
                        val progress = (bytesSentTotal.toDouble() / contentLength * 100).toInt()
                        progressIndicator.progress = progress
                    }
                }
            }
            if (response.status.value in 200..299) {
                val release: GitHubRelease = response.body()

                val directLink = if (artifactName != "null.apk") {
                    release.assets.firstOrNull { it.name.contains(artifactName) }?.browserDownloadUrl
                } else {
                    release.assets.firstOrNull { it.name.endsWith(".apk", ignoreCase = true) }?.browserDownloadUrl
                }
                val tagName = release.tagName

                Pair(directLink, tagName)
            } else {
                progressDialog.dismiss()
                showErrorDialog("Server Error", "An error occurred while communicating with the server. Please try again later.")
                Pair(null, null)
            }
        } catch (e: IOException) {
            progressDialog.dismiss()
            showErrorDialog("Network Error", "Unable to connect to the internet. Please check your network connection and try again.")
            Pair(null, null)
        } finally {
            progressDialog.dismiss()
        }
    }

    fun close() {
        client.close()
    }

    private fun showErrorDialog(dialogTitle: String, dialogMessage: String) {
        MaterialAlertDialogBuilder(context)
            .setTitle(dialogTitle)
            .setMessage(dialogMessage)
            .setPositiveButton("Retry") { dialog, which ->
                dialog.dismiss() 
                // TODO: Implement a logic to perform retry
            }
            .setCancelable(false)
            .show()
    }
}
