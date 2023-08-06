# Never mind regedit.exe, here is reg2df

```python
$pip install a-pandas-ex-reg2df 
from a_pandas_ex_reg2df import pd_add_reg2df
pd_add_reg2df()
import pandas as pd

pd.Q_get_installed_apps()
Microsoft (R) Windows Script Host Version 5.812
Copyright (C) Microsoft Corporation. All rights reserved.
Out[6]: 
                                     Caption  ...         Version
0                                Pandoc 2.16  ...            2.16
1                 MDI To TIFF File Converter  ...  12.0.6661.5002
2            Microsoft DCF MUI (German) 2016  ...  16.0.4266.1001
3    Microsoft Office Professional Plus 2016  ...  16.0.4266.1001
4        Microsoft OneNote MUI (German) 2016  ...  16.0.4266.1001
..                                       ...  ...             ...
262     Windows Team Extension SDK Contracts  ...  10.1.19041.685
263                       vs_communitymsires  ...     16.10.31213
264                Windows IoT Extension SDK  ...  10.1.19041.685
265           WinRT Intellisense PPI - en-us  ...  10.1.19041.685
266          Windows SDK Desktop Tools arm64  ...    10.1.22621.1
[267 rows x 10 columns]


In[8]: pd.Q_get_HKLM_df()
The operation completed successfully.
Out[8]: 
                                                        0               
0              HKEY_LOCAL_MACHINE\BCD00000000\Description  "KeyName"="BC
1       HKEY_LOCAL_MACHINE\BCD00000000\Objects\{0ce0f4...  "Type"=dword:
2       HKEY_LOCAL_MACHINE\BCD00000000\Objects\{0ce0f4...               
3       HKEY_LOCAL_MACHINE\BCD00000000\Objects\{0ce0f4...               
4       HKEY_LOCAL_MACHINE\BCD00000000\Objects\{0ce0f4...  "Element"=hex
                                                   ...                  
515916  HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Se...  "QueryAlias"=
515917  HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Se...  "QueryAlias"=
515918  HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Se...  "QueryAlias"=
515919  HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Se...  "QueryAlias"=
515920  HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Se...  "QueryAlias"=
[515921 rows x 2 columns]


In[9]: pd.Q_get_HKU_df()
The operation completed successfully.
Out[9]: 
                                                       0                  
0      HKEY_USERS\.DEFAULT\Control Panel\Accessibilit...                  
1      HKEY_USERS\.DEFAULT\Control Panel\Accessibilit...           "Flags"
2      HKEY_USERS\.DEFAULT\Control Panel\Accessibilit...                  
3      HKEY_USERS\.DEFAULT\Control Panel\Accessibilit...  "AutoRepeatDelay
4      HKEY_USERS\.DEFAULT\Control Panel\Accessibilit...  "Flags"="62"\n"M
                                                  ...                     
74501  HKEY_USERS\S-1-5-18\Software\Trolltech\Organiz...  "qgif4.dll"=hex(
74502  HKEY_USERS\S-1-5-18\Software\Trolltech\Organiz...  "qgif4.dll"=hex(
74503  HKEY_USERS\S-1-5-18\Software\Trolltech\Organiz...  "qgif4.dll"=hex(
74504           HKEY_USERS\S-1-5-18\Software\Valve\Steam                  
74505  HKEY_USERS\S-1-5-18\System\CurrentControlSet\C...                  
[74506 rows x 2 columns]


In[10]: pd.Q_get_HKCR_df()
The operation completed successfully.
Out[10]: 
                                                        0                                    
0                                     HKEY_CLASSES_ROOT\                                @=".
1                                     HKEY_CLASSES_ROOT\*  "AlwaysShowExt"=""\n"ConflictPromp
2               HKEY_CLASSES_ROOT\*\OpenWithList\gvim.exe                                    
3            HKEY_CLASSES_ROOT\*\OpenWithList\MSPaint.exe                                    
4            HKEY_CLASSES_ROOT\*\OpenWithList\notepad.exe                                    
                                                   ...                                       
229577  HKEY_CLASSES_ROOT\{B9B39BF7-DB16-4B26-AAD0-D23...  "ExperimentId"="spotlight"\n"Exper
229578                          HKEY_CLASSES_ROOT\Ŭ伵탞ࠀ耀ṰԐ                                   @
229579                      HKEY_CLASSES_ROOT\౵ხ惿退contact                                @=".
229580                                HKEY_CLASSES_ROOT\๼                                 @="
229581                             HKEY_CLASSES_ROOT\ﷆˤࣼ踀                                  @=
[229582 rows x 2 columns]


pd.Q_get_HKCC_df()
The operation completed successfully.
Out[11]: 
                                                   0                                  1
0                 HKEY_CURRENT_CONFIG\Software\Fonts         "LogPixels"=dword:00000060
1  HKEY_CURRENT_CONFIG\System\CurrentControlSet\C...     "PrinterOnLine"=dword:00000001
2  HKEY_CURRENT_CONFIG\System\CurrentControlSet\C...     "PrinterOnLine"=dword:00000001
3  HKEY_CURRENT_CONFIG\System\CurrentControlSet\S...  "Attach.ToDesktop"=dword:00000001



df=pd.Q_get_exefiles_df()

Out[3]: 
                                             file_path
0    C:\\Program Files\\Locktime Software\\NetLimit...
1    C:\\Program Files\\Internet Explorer\\iexplore...
2    C:\\Program Files (x86)\\FileMarker.NET\\FileM...
3          C:\\Program Files\\Notepad++\\notepad++.exe
4    C:\\Program Files (x86)\\BlueStacks X\\BlueSta...
..                                                 ...
106  C:\\Riot Games\\VALORANT\\live\\ShooterGame\\B...
107  F:\\SteamLibrary33\\steamapps\\common\\Doki Do...
108  C:\\Users\\Gamer\\AppData\\Roaming\\.minecraft...
109  E:\\Spiele\\Battle.net\\Destiny 2\\Overwatch\\...
110            E:\\Spiele\\Far Cry 5\\bin\\FarCry5.exe
[111 rows x 1 columns]

```