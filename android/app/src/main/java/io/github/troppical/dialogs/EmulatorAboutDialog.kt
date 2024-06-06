package io.github.troppical.dialogs

import android.content.Context
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
import java.io.File

class EmulatorAboutDialog(context: Context, private val activity: Activity, private val item: HashMap<String, Any>) : BaseSheetDialog(context) {

    private val fetcherScope = CoroutineScope(Dispatchers.Main + Job())
    private lateinit var downloadUrl: String
    private var apkPath: File? = null
    private var tagName: String? = null
    private var install

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.emulator_about_dialog)

        val emulatorName = findViewById<TextView>(R.id.emulator_name)
        val emulatorDesc = findViewById<TextView>(R.id.emulator_desc)
        val emulatorLogo = findViewById<ImageView>(R.id.emulator_logo)
        val emulatorLatestVersion = findViewById<TextView>(R.id.emulator_latest_version)
        val installButton = findViewById<MaterialButton>(R.id.install)

        if (isAppInstalled(item["emulator_package"].toString())) {
            installButton.setText("Update")
        }      

        emulatorName.text = item["emulator_name"].toString()
        emulatorDesc.text = item["emulator_desc"].toString()
        Glide.with(context).load(Uri.parse(item["emulator_logo"].toString())).into(emulatorLogo)

        fetcherScope.launch {
            val fetcher = GitHubReleaseFetcher(item["emulator_owner"].toString(), item["emulator_repo"].toString())
            try {
                val artifactName = item["emulator_artifact_name"].toString()
                val (directLink, tag) = fetcher.fetchArtifactDirectLinkAndTag(artifactName)
                tagName = tag
                emulatorLatestVersion.text = tag

                updateInstallButtonText(installButton)

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
        
        installButton.setOnClickListener {
           install()
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
                            installer.install(outputFile)
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
                                            apkFilePath?.let { installer.install(it) }
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
                        installButton.setText("Update")
                    } else {
                        installButton.setText("Open")
                    }
                } else {
                    installButton.setText("Update")
                }
            } else {
                installButton.setText("Install")
            }
        } else {
            installButton.setText("Install")
        }
    }

    private fun getInstalledAppVersion(packageName: String): String? {
        return try {
            val packageInfo = context.packageManager.getPackageInfo(packageName, 0)
            packageInfo.versionName
        } catch (e: PackageManager.NameNotFoundException) {
            null
        }
    }

    private fun isVersionFormat(version: String): Boolean {
        val versionRegex = Regex("""\d+\.\d+\.\d+""")
        return versionRegex.matches(version)
    }

    private fun compareVersions(version1: String, version2: String): Int {
        val parts1 = version1.split(".").map { it.toInt() }
        val parts2 = version2.split(".").map { it.toInt() }

        for (i in parts1.indices) {
            if (parts1[i] != parts2[i]) {
                return parts1[i] - parts2[i]
            }
        }
        return 0
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
