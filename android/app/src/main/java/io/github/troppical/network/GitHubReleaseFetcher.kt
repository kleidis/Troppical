package io.github.troppical.network

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

class GitHubReleaseFetcher(private val owner: String, private val repo: String) {

    private val client = HttpClient(CIO) {
        install(ContentNegotiation) {
            json(Json { ignoreUnknownKeys = true })
        }
    }

    suspend fun fetchArtifactDirectLinkAndTag(artifactName: String): Pair<String?, String?> {
        val url = "https://api.github.com/repos/$owner/$repo/releases"
        val response: HttpResponse = client.get(url)
        val releases: List<GitHubRelease> = response.body()

        val latestReleaseOrPreRelease = releases
            .sortedWith(compareByDescending<GitHubRelease> { it.prerelease }.thenByDescending { it.tagName })
            .firstOrNull()

        val directLink = latestReleaseOrPreRelease?.assets?.firstOrNull { it.name.contains(artifactName) }?.browserDownloadUrl
        val tagName = latestReleaseOrPreRelease?.tagName

        return Pair(directLink, tagName)
    }

    fun close() {
        client.close()
    }
}
