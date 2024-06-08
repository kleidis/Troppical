package io.github.troppical.network

import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.util.Log

class AppUninstallReceiver(
    private val onComplete: () -> Unit,
    private val onFailure: (Exception) -> Unit
) : BroadcastReceiver() {

    override fun onReceive(context: Context, intent: Intent) {
        val packageName = intent.data?.schemeSpecificPart
        when (intent.action) {
            Intent.ACTION_PACKAGE_REMOVED -> {
                Log.i("AppUninstallReceiver", "Package uninstalled: $packageName")
                onComplete()
                context.unregisterReceiver(this)
            }
            else -> {
                onFailure(Exception("Uninstallation failed for package: $packageName"))
                context.unregisterReceiver(this)
            }
        }
    }
}
