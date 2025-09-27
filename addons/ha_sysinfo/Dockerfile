diff --git a/addons/ha_sysinfo/Dockerfile b/addons/ha_sysinfo/Dockerfile
index 3c5c1f1..a9f4f9a 100644
--- a/addons/ha_sysinfo/Dockerfile
+++ b/addons/ha_sysinfo/Dockerfile
@@
 ARG BUILD_FROM=ghcr.io/hassio-addons/base:15.0.6
 FROM ${BUILD_FROM}

-WORKDIR /usr/src/app
-
-# Kopier kode
-# (mangler i originalen, derfor finner den ikke /run.sh)
-
-# Default kommando
-CMD [ "/run.sh" ]
+WORKDIR /usr/src/app
+
+# Kopier run.sh inn i containeren
+COPY run.sh /run.sh
+RUN chmod a+x /run.sh
+
+# Default kommando
+CMD [ "/run.sh" ]
