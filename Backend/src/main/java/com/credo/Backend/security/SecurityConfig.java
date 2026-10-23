
package com.credo.backend.security;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configurers.AbstractHttpConfigurer;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.core.authority.AuthorityUtils;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.authentication.UsernamePasswordAuthenticationFilter;
import org.springframework.web.filter.OncePerRequestFilter;

import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;

@Configuration
public class SecurityConfig {

    @Bean
    public ApiKeyAuthFilter apiKeyAuthFilter(
            @Value("${credo.api-key:}") String configuredApiKey) {
        return new ApiKeyAuthFilter(configuredApiKey);
    }

    @Bean
    public SecurityFilterChain securityFilterChain(
            HttpSecurity http,
            ApiKeyAuthFilter apiKeyAuthFilter) throws Exception {

        http
                .csrf(AbstractHttpConfigurer::disable)
                .sessionManagement(session -> session
                        .sessionCreationPolicy(SessionCreationPolicy.STATELESS))
                .authorizeHttpRequests(auth -> auth
                        .requestMatchers("/error").permitAll()
                        .anyRequest().authenticated())
                .addFilterBefore(
                        apiKeyAuthFilter,
                        UsernamePasswordAuthenticationFilter.class);

        return http.build();
    }

    public static class ApiKeyAuthFilter extends OncePerRequestFilter {

        private final String configuredApiKey;

        public ApiKeyAuthFilter(String configuredApiKey) {
            this.configuredApiKey = configuredApiKey;
        }

        @Override
        protected boolean shouldNotFilter(HttpServletRequest request) {
            return "/error".equals(request.getServletPath());
        }

        @Override
        protected void doFilterInternal(
                HttpServletRequest request,
                HttpServletResponse response,
                FilterChain filterChain)
                throws ServletException, IOException {

            String suppliedKey = request.getHeader("X-API-Key");

            if (configuredApiKey == null || configuredApiKey.isBlank()
                    || suppliedKey == null
                    || !MessageDigest.isEqual(
                            configuredApiKey.getBytes(StandardCharsets.UTF_8),
                            suppliedKey.getBytes(StandardCharsets.UTF_8))) {

                response.setStatus(HttpServletResponse.SC_UNAUTHORIZED);
                response.setContentType("application/json");
                response.getWriter().write(
                        "{\"error\":\"Invalid or missing API key\"}");
                return;
            }

            var authentication =
                    new UsernamePasswordAuthenticationToken(
                            "lender-api-client",
                            null,
                            AuthorityUtils.NO_AUTHORITIES);

            org.springframework.security.core.context.SecurityContextHolder
                    .getContext().setAuthentication(authentication);

            filterChain.doFilter(request, response);
        }
    }
}
