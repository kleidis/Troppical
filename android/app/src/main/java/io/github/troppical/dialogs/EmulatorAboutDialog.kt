package io.github.troppical.dialogs

import android.content.Context
import android.content.BroadcastReceiver
import android.content.Intent
import android.content.IntentFilter
import android.os.Bundle
import android.app.Activity
import android.content.pm.PackageManager
import android.net.Uri
import android.util.Log
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.CompoundButton
import android.widget.ImageView
import android.widget.TextView
import com.google.android.material.button.MaterialButton
import com.google.android.material.dialog.MaterialAlertDialogBuilder
import com.google.android.material.progressindicator.LinearProgressIndicator
import kotlinx.coroutines.*
import com.bumptech.glide.Glide
import io.github.troppical.R
import io.github.troppical.network.GitHubReleaseFetcher
import io.github.troppical.network.APKDownloader
import io.github.troppical.network.APKInstaller
import io.github.troppical.utils.ZipExtractor
import io.github.troppical.network.AppUninstallReceiver
import java.io.File

class EmulatorAboutDialog(context: Context, private val activity: Activity, private val item: HashMap<String, Any>) : BaseSheetDialog(context) {

    private val fetcherScope = CoroutineScope(Dispatchers.Main + Job())
    private lateinit var downloadUrl: String
    private var apkPath: File? = null
    private var tagName: String? = null
    private var isOpenEnabled: Boolean = false
    private var isUnInstallable: Boolean = false

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.emulator_about_dialog)

        val emulatorName = findViewById<TextView>(R.id.emulator_name)
        val emulatorDesc = findViewById<TextView>(R.id.emulator_desc)
        val emulatorLogo = findViewById<ImageView>(R.id.emulator_logo)
        val emulatorLatestVersion = findViewById<TextView>(R.id.emulator_latest_version)
        val installButton = findViewById<MaterialButton>(R.id.install)  
        val unInstallButton = findViewById<MaterialButton>(R.id.uninstall)

        emulatorName.text = item["emulator_name"].toString()
        emulatorDesc.text = item["emulator_desc"].toString()
        Glide.with(context).load(Uri.parse(item["emulator_logo"].toString())).into(emulatorLogo)
        unInstallButton.visibility = View.GONE

        fetchGitHubRelease()
        
        installButton.setOnClickListener {
            if (isOpenEnabled) {
                openApp(item["emulator_package"].toString())
            } else {
                install()
            }
        }

        unInstallButton.setOnClickListener {
            uninstallApp(item["emulator_package"].toString(),
                onComplete = {
                    Log.i("EmulatorAboutDialog", "Uninstallation succeeded")
                    fetchGitHubRelease()
                },
                onFailure = { e ->
                    Log.w("EmulatorAboutDialog", "Uninstallation failed", e)
                    // nothing to do
                }
            )
        }
    }

    private fun install() {
        val outputFile = File(context.filesDir, item["emulator_artifact_name"].toString())
        val downloader = APKDownloader(downloadUrl, outputFile)

        val progressDialog = MaterialAlertDialogBuilder(context)
            .setTitle("Downloading")
            .setView(R.layout.progress_dialog)
            .setCancelable(false)
            .create()

        val progressIndicator: LinearProgressIndicator

        progressDialog.show()
        progressIndicator = progressDialog.findViewById(R.id.progress_indicator)!!

        downloader.download(
            onProgress = { progress ->
                activity.runOnUiThread {
                    progressIndicator.progress = progress
                }
            },
            onComplete = { success ->
                activity.runOnUiThread {
                    progressDialog.dismiss()
                    if (success) {
                        if (outputFile.extension.equals("apk", ignoreCase = true)) {
                            val installer = APKInstaller(context)
                            installer.install(outputFile,
                                onComplete = {
                                    Log.i("EmulatorAboutDialog", "Installation succeeded")
                                    fetchGitHubRelease()
                                    apkPath?.let {
                                        if (it.exists()) {
                                            it.delete() // Ensure that the apk is deleted after installation 
                                        }
                                    }
                                },
                                onFailure = { e ->
                                    Log.e("EmulatorAboutDialog", "Installation failed", e)
                                    apkPath?.let {
                                        if (it.exists()) {
                                            it.delete() // Ensure that the apk is deleted after installation failed
                                        }
                                    }
                                }
                            )
                            apkPath = outputFile
                        } else {
                            val progressDialogExtract = MaterialAlertDialogBuilder(context)
                                .setTitle("Extracting")
                                .setView(R.layout.progress_dialog)
                                .setCancelable(false)
                                .create()

                            progressDialogExtract.show()
                            val progressIndicatorExtract = progressDialogExtract.findViewById<LinearProgressIndicator>(R.id.progress_indicator)!!

                            val zipExtractor = ZipExtractor(
                                zipFilePath = outputFile, 
                                destDirectory = context.filesDir,
                                progressCallback = { progress ->
                                    activity.runOnUiThread {
                                        progressIndicatorExtract.progress = progress
                                    }
                                },
                                onComplete = { success, apkFilePath ->
                                    outputFile.delete()
                                    apkPath = apkFilePath
                                    activity.runOnUiThread {
                                        progressDialogExtract.dismiss()
                                        if (success && apkFilePath != null) {
                                            val installer = APKInstaller(context)
                                            apkFilePath?.let { installer.install(it,
                                            onComplete = {
                                                Log.i("EmulatorAboutDialog", "Installation succeeded")
                                                fetchGitHubRelease()
                                                apkPath?.let {
                                                    if (it.exists()) {
                                                        it.delete() // Ensure that the apk is deleted after installation 
                                                    }
                                                }
                                            },
                                            onFailure = { e ->
                                                Log.e("EmulatorAboutDialog", "Installation failed", e)
                                                apkPath?.let {
                                                    if (it.exists()) {
                                                        it.delete() // Ensure that the apk is deleted after installation failed
                                                    }
                                                }
                                            }
                                        ) }
                                        } else {
                                            // TODO: Handle extraction failure
                                            Log.e("EmulatorAboutDialog", "Extraction failed or no APK file found.")
                                        }
                                    }
                                }
                            )

                            CoroutineScope(Dispatchers.IO).launch {
                                zipExtractor.extract()
                            }
                        }      
                    } else {
                        // TODO: Handle download failure
                        Log.e("EmulatorAboutDialog", "Download failed.")
                    }
                }
            }
        )
    }

    private fun uninstallApp(packageName: String, onComplete: () -> Unit, onFailure: (Exception) -> Unit) {
        try {
            val intent = Intent(Intent.ACTION_DELETE)
            intent.data = Uri.parse("package:$packageName")
            intent.flags = Intent.FLAG_ACTIVITY_NEW_TASK

            // Listen for uninstallation result
            val receiver = AppUninstallReceiver(onComplete, onFailure)
            context.registerReceiver(receiver, IntentFilter().apply {
                addAction(Intent.ACTION_PACKAGE_REMOVED)
                addDataScheme("package")
            })

            context.startActivity(intent)
        } catch (e: Exception) {
            onFailure(e)
        }
   }



    private fun openApp(packageName: String) {
        val launchIntent: Intent? = context.packageManager.getLaunchIntentForPackage(packageName)
        if (launchIntent != null) {
            context.startActivity(launchIntent)
        } else {
            Log.e("EmulatorAboutDialog", "Cannot open app with package name $packageName")
        }
    }
        

    private fun isAppInstalled(packageName: String): Boolean {
        return try {
            val packageInfo = context.packageManager.getPackageInfo(packageName, PackageManager.GET_ACTIVITIES)
            Log.i("EmulatorAboutDialog", "Package ${packageInfo.packageName} is installed.")
            true
        } catch (e: PackageManager.NameNotFoundException) {
            Log.i("EmulatorAboutDialog", "Package $packageName is not installed.")
            false
        }
    }

    private fun updateInstallButtonText(installButton: MaterialButton) {
        val packageName = item["emulator_package"].toString()
        if (isAppInstalled(packageName)) {
            val installedVersion = getInstalledAppVersion(packageName)
            val fetchedVersion = tagName?.removePrefix("v")
            
            if (fetchedVersion != null && isVersionFormat(fetchedVersion)) {
                if (installedVersion != null && isVersionFormat(installedVersion)) {
                    if (compareVersions(installedVersion, fetchedVersion) < 0) {
                        installButton.setText(R.string.update)
                        isOpenEnabled = false
                        isUnInstallable = true
                    } else {
                        installButton.setText(R.string.open)
                        isOpenEnabled = true
                        isUnInstallable = true
                    }
                } else {
                    installButton.setText(R.string.update)
                    isOpenEnabled = false
                    isUnInstallable = true
                }
            } else {
                installButton.setText(R.string.install)
                isOpenEnabled = false
                isUnInstallable = false
            }
        } else {
            installButton.setText(R.string.install)
            isOpenEnabled = false
            isUnInstallable = false
        }
    }

    private fun getInstalledAppVersion(packageName: String): String? {
        return try {
            val packageInfo = context.packageManager.getPackageInfo(packageName, 0)
            if (item["emulator_package"].toString() == "org.vita3k.emulator") {
                packageInfo.versionName.split("-").getOrNull(1)
            } else {
                packageInfo.versionName
            }
        } catch (e: PackageManager.NameNotFoundException) {
            null
        }
    }

    private fun isVersionFormat(version: String): Boolean {
        val versionRegex = Regex("""\d+(\.\d+){1,2}(-rc\d+)?""")
        return if (item["emulator_package"].toString() == "org.vita3k.emulator") {
            true
        } else {
            versionRegex.matches(version)
        }
    }


    private fun compareVersions(version1: String, version2: String): Int {
        val versionRegex = Regex("""(\d+(\.\d+){1,2})(-rc(\d+))?""")

        val match1 = versionRegex.matchEntire(version1)
        val match2 = versionRegex.matchEntire(version2)

        if (match1 != null && match2 != null) {
            val baseVersion1 = match1.groupValues[1]
            val baseVersion2 = match2.groupValues[1]

            val parts1 = baseVersion1.split(".").map { it.toIntOrNull() ?: 0 }
            val parts2 = baseVersion2.split(".").map { it.toIntOrNull() ?: 0 }

            val maxLength = maxOf(parts1.size, parts2.size)
            val paddedParts1 = parts1 + List(maxLength - parts1.size) { 0 }
            val paddedParts2 = parts2 + List(maxLength - parts2.size) { 0 }

            for (i in 0 until maxLength) {
                if (paddedParts1[i] != paddedParts2[i]) {
                    return paddedParts1[i] - paddedParts2[i]
                }
            }

            // Compare RC versions if base versions are equal
            val rcVersion1 = match1.groupValues[4].toIntOrNull() ?: Int.MAX_VALUE
            val rcVersion2 = match2.groupValues[4].toIntOrNull() ?: Int.MAX_VALUE

            return rcVersion1 - rcVersion2
        }
        return 0
   }


    private fun fetchGitHubRelease() {
        val emulatorLatestVersion = findViewById<TextView>(R.id.emulator_latest_version)
        val installButton = findViewById<MaterialButton>(R.id.install)  
        val unInstallButton = findViewById<MaterialButton>(R.id.uninstall)
        
        fetcherScope.launch {
            val fetcher = GitHubReleaseFetcher(item["emulator_owner"].toString(), item["emulator_repo"].toString(), context)
            try {
                val artifactName = item["emulator_artifact_name"].toString()
                val (directLink, tag) = fetcher.fetchArtifactDirectLinkAndTag(artifactName)
                tagName = tag
                emulatorLatestVersion.text = tag
                
                updateInstallButtonText(installButton)
                if (isUnInstallable) {
                    unInstallButton.visibility = View.VISIBLE
                } else {
                    unInstallButton.visibility = View.GONE
                }

                if (directLink != null) {
                    downloadUrl = directLink 
                    Log.w("EmulatorAboutDialog", "Direct download link is $directLink")
                } else {
                    Log.e("EmulatorAboutDialog", "Artifact not found")
                }
            } catch (e: Exception) {
                Log.e("EmulatorAboutDialog", "Error fetching version", e)
                emulatorLatestVersion.text = "Error fetching version"
            } finally {
                fetcher.close()
            }
        }
    }
        

    override fun onStop() {
        super.onStop()
        apkPath?.let {
            if (it.exists()) {
                it.delete() // Ensure that the apk is deleted when no longer needed
            }
        }
        fetcherScope.cancel() // Cancel any ongoing coroutines when the dialog is destroyed
    }
}
