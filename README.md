# SMS to Telegram Bot

This project allows you to receive SMS messages on an Ubuntu server using a SIM800 GSM modem and forward them to a Telegram bot.

### Setup

 **Install Dependencies**
   - Install Python 3 and pip if not already installed.
   - Install required Python packages: `requests`
   - Install Gammu and Gammu SMSD:
     ```bash
     sudo apt-get update
     sudo apt-get install gammu gammu-smsd
     ```

 **Configure Gammu and SMSD**

   - Connect your SIM800 GSM modem to your Ubuntu server via USB.
   - Determine the modem's port (usually `/dev/ttyUSB0`). You can check this using:
     ```bash
     ls /dev/ttyUSB*
     ```
     Note down the port (e.g., `/dev/ttyUSB0`).

   - Edit `gammu-smsdrc` with your modem settings (`/etc/gammu-smsdrc`). Here's an example configuration:
     ```ini
     # Configuration file for Gammu SMS Daemon

     [gammu]
     port = /dev/ttyUSB0
     connection = at115200
     logfile = /var/log/smsd/gammu.log
     logformat = textall

     [smsd]
     service = files
     inboxpath = /var/spool/gammu/inbox/
     outboxpath = /var/spool/gammu/outbox/
     sentsmspath = /var/spool/gammu/sent/
     errorsmspath = /var/spool/gammu/error/
     inboxformat = unicode
     outboxformat = unicode
     transmitformat = auto
     debuglevel = 1
     pin =
     logfile = /var/log/smsd/smsd.log
     multiparttimeout = 20
     hangupcalls = 1
     deliveryreport = sms
     deliveryreportdelay = 7200
     resetfrequency = 3600
     checksecurity = 0
     resetfrequency = 14400
     phoneid = SIM800C
     runonreceive = /usr/bin/python3 /path/to/your_script.py
     ```

     **Create Log Directory**

     Make sure the directory `/var/log/smsd/` exists. If not, create it:

     ```bash
     sudo mkdir -p /var/log/smsd
     sudo chown gammu:gammu /var/log/smsd
     sudo chmod 755 /var/log/smsd

     ```
     
   - Make the python script executable:
     ```bash
     chmod +x send_sms_to_telegram.py
     ```
     
  **Testing Modem Connection and Signal Strength**

   - **Check Modem Connection**: Ensure your modem is correctly detected and connected to `/dev/ttyUSB0`. You can check this by listing all USB devices (`ls /dev/ttyUSB*`).

   - **Test Signal with `minicom`**:
     - Install `minicom` if not already installed:
       ```bash
       sudo apt-get install minicom
       ```

     - Open `minicom` to test the modem's signal strength and functionality:
       ```bash
       sudo minicom -b 9600 -o -D /dev/ttyUSB0
       ```

     - Inside `minicom`, test AT commands (e.g., check signal strength):
       ```
       AT
       AT+CSQ
       ```

     - Press `Ctrl+A` followed by `X` to exit `minicom`.


     **Injecting a Test SMS**

     To inject a command to send an SMS using Gammu's `gammu-smsd-inject` tool for testing purposes, follow these steps:

     **Open a Terminal**

     Open your terminal application on your Ubuntu server.

     **Inject Command**

     Replace `<destination_number>` with the phone number where you want to send the test SMS, and `"Your message here"` with the actual message you want to send.

     ```bash
     gammu-smsd-inject TEXT <destination_number> -text "This is a test message."
     ```

  **Run**

   - Start the Gammu SMS Daemon service:
     ```bash
     sudo systemctl enable gammu-smsd.service
     sudo systemctl start gammu-smsd.service
     sudo systemctl status gammu-smsd.service
     ```

 **Troubleshooting**

 ```bash
 sudo systemctl start gammu-smsd.service
 ```
   - Check logs for Gammu: `/var/log/smsd/gammu.log`
   - Check SMSD logs: `/var/log/smsd/smsd.log`

 **Contributing**
   - Contributions are welcome! Fork the repository and submit pull requests.

### Notes

- Ensure proper security practices when handling sensitive information like API tokens.
- Customize paths and settings in scripts according to your setup.
