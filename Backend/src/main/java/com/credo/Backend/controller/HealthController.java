
package com.credo.backend.controller;
import org.springframework.http.ResponseEntity;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import java.time.Instant;
import java.util.Map;

@RestController
public class HealthController {

    @Value("${spring.profiles.active:default}")
    private String environment;

    @GetMapping("/health")
public ResponseEntity<Map<String, String>> health() {
    Map<String, String> response = Map.of(
            "status", "UP",
            "service", "CREDO Backend",
            "version", "1.0.0",
            "environment", environment,
            "timestamp", Instant.now().toString()
    );

    return ResponseEntity.ok()
            .header("X-Service-Name", "CREDO Backend")
            .body(response);
}
}
