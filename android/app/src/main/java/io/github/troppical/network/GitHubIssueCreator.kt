package io.github.troppical.network

import okhttp3.MediaType.Companion.toMediaTypeOrNull
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.RequestBody.Companion.toRequestBody
import okhttp3.Response
import com.google.gson.Gson

// Data class to represent an Issue
data class Issue(
    val title: String,
    val body: String
)

class GitHubIssueCreator {
    private val client = OkHttpClient()
    private val gson = Gson()

    fun createIssue(repo: String, issue: Issue): Response {
        val json = gson.toJson(issue)
        val body = json.toRequestBody("application/json; charset=utf-8".toMediaTypeOrNull())

        val request = Request.Builder()
            .url("https://api.github.com/repos/$repo/issues")
            .post(body)
            .build()

        return client.newCall(request).execute()
    }
}
