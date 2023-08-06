<h2>Python ShadowCopy Class</h2>

<p>Python ShadowCopy Analyzer for Cyber Security Researchers!<br>pip install reshadowcode</p>

<h2>Images</h2>
<img src="https://learn.microsoft.com/en-us/windows-server/storage/file-server/media/volume-shadow-copy-service/ee923636.94dfb91e-8fc9-47c6-abc6-b96077196741(ws.10).jpg" />
<br>
<img src="https://learn.microsoft.com/en-us/windows-server/storage/file-server/media/volume-shadow-copy-service/ee923636.1c481a14-d6bc-4796-a3ff-8c6e2174749b(ws.10).jpg" />
<h2>Example Code</h2>

<pre>
# List all ShadowCopy
'''
Example Result
ID : {e9a894be-dae7-49cb-9196-b5a22148210b}
Creation Date : 6.11.2022 19:58:20
Shadow Copy Location : \\?\GLOBALROOT\Device\HarddiskVolumeShadowCopy7
'''
list = pyshadow.VSS_ListShadows()
for shadowlist in list:
    print("ID : " + shadowlist["id"] + "\nCreation Date : " + shadowlist["creation_time"] + "\nShadow Copy Location : " + shadowlist["shadowcopy"] + "\n")
#Create a ShadowCopy
pyshadow.VSS_Create()
#Create a pipe/symlink with ShadowCopy()
pyshadow.VSS_Create_Pipe("C:\\Shadow1", "7")
#Get file list from ShadowCopy
'''
Example Result
ID : {e9a894be-dae7-49cb-9196-b5a22148210b}
Creation Date : 6.11.2022 19:58:20
Shadow Copy Location : \\?\GLOBALROOT\Device\HarddiskVolumeShadowCopy7
'''
list = pyshadow.VSS_Get_FileList("C:\\Shadow1\\Users")
for files in list:
    print(files)
</pre>