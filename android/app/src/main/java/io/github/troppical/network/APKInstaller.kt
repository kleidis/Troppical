package io.github.troppical.network

import android.content.Context
import android.content.Intent
import android.net.Uri
import androidx.core.content.FileProvider
import java.io.File

class APKInstaller(private val context: Context) {

    fun install(apkFile: File) {
        val apkUri: Uri = FileProvider.getUriForFile(
            context,
            context.applicationContext.packageName + ".provider",
            apkFile
        )
        val intent = Intent(Intent.ACTION_VIEW)
        intent.setDataAndType(apkUri, "application/vnd.android.package-archive")
        intent.flags = Intent.FLAG_GRANT_READ_URI_PERMISSION or Intent.FLAG_ACTIVITY_NEW_TASK
        context.startActivity(intent)
    }
}
