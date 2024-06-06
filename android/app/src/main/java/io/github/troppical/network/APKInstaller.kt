package io.github.troppical.network

import android.content.Context
import android.content.Intent
import android.content.IntentFilter
import android.content.pm.PackageInstaller
import android.net.Uri
import androidx.core.content.FileProvider
import kotlinx.coroutines.GlobalScope
import kotlinx.coroutines.launch
import java.io.File

class APKInstaller(private val context: Context) {

    fun install(apkFile: File, onComplete: () -> Unit, onFailure: (Exception) -> Unit) {
        try {
            val apkUri: Uri = FileProvider.getUriForFile(
                context,
                context.applicationContext.packageName + ".provider",
                apkFile
            )
            val intent = Intent(Intent.ACTION_VIEW)
            intent.setDataAndType(apkUri, "application/vnd.android.package-archive")
            intent.flags = Intent.FLAG_GRANT_READ_URI_PERMISSION or Intent.FLAG_ACTIVITY_NEW_TASK
            context.startActivity(intent)

            // Listen for installation result
            GlobalScope.launch {
                val receiver = AppInstallReceiver(onComplete, onFailure)
                context.registerReceiver(receiver, IntentFilter().apply {
                    addAction(Intent.ACTION_PACKAGE_ADDED)
                    addAction(Intent.ACTION_PACKAGE_REPLACED)
                    addDataScheme("package")
                })
            }
        } catch (e: Exception) {
            onFailure(e)
        }
    }
}
