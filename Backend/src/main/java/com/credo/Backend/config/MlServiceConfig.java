
package com.credo.backend.config;

import org.springframework.boot.context.properties.ConfigurationProperties;

@ConfigurationProperties(prefix = "credo.ml")
public record MlServiceConfig(
        String baseUrl
) {}
