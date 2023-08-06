VENDOR_DIR := "songmanager/static/vendor"

.PHONY: download_vendor_libs
download_vendor_libs:
	curl -o $(VENDOR_DIR)/htmx.min.js https://unpkg.com/htmx.org@1.9.4/dist/htmx.min.js
	curl -L -o $(VENDOR_DIR)/bootstrap-5.3.1-dist.zip https://github.com/twbs/bootstrap/releases/download/v5.3.1/bootstrap-5.3.1-dist.zip
	unzip $(VENDOR_DIR)/bootstrap-5.3.1-dist.zip -d $(VENDOR_DIR)
	rm $(VENDOR_DIR)/bootstrap-5.3.1-dist.zip