## Wazuh與PfSense主動防禦機制 

本專案實作了 **Wazuh + pfSense** 的自動化聯防機制。當 Wazuh 偵測到 SSH 暴力破解攻擊時，會自動觸發 Active Response，透過 SSH 連線至 pfSense 防火牆封鎖攻擊來源。

### 1. 架構說明
* **Wazuh Manager**: 負責監控日誌，偵測 `Rule ID: 5716` 。
* **Active Response Script**: 使用 Python (`paramiko`) 撰寫腳本，負責與防火牆溝通。
* **pfSense Firewall**: 接收指令並執行 `easyrule block` 封鎖 IP。

### 2. 實作檔案 (Files)
* [pfsense_block.py](pfsense_block.py): 自動封鎖腳本，部署於 `/var/ossec/active-response/bin/`。
* [ossec_config.xml](ossec_config.xml): Wazuh 設定檔片段，定義觸發條件與執行命令。

### 3. 環境截圖 (Screenshot)
pfSense 防火牆已成功部署並與 Wazuh 位於同一內網 (192.168.56.x)。


![pfSense Running](firewallpic1)
