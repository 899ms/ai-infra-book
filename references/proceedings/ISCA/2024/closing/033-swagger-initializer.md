<!-- 从 033-swagger-initializer.html 迁移的资料快照；原始 HTML SHA-256: a04bd58381fd53b1902caa99138f3f2bb5f5af705649be5620185317453408df。 -->

window.onload = function() { // // the following lines will be replaced by docker/configurator, when it runs in a docker-container window.ui = SwaggerUIBundle({ url: './docs/openapi.yaml', dom_id: '#swagger-ui', deepLinking: true, presets: \[ SwaggerUIBundle.presets.apis, SwaggerUIStandalonePreset \], plugins: \[ SwaggerUIBundle.plugins.DownloadUrl \], layout: "StandaloneLayout" }); // };
