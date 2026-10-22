
package com.credo.backend.security;

import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Component;

@Component
public class CurrentLender {

    public LenderPrincipal get() {
        Authentication authentication =
                SecurityContextHolder.getContext().getAuthentication();

        if (authentication == null
                || !authentication.isAuthenticated()
                || !(authentication.getPrincipal()
                instanceof LenderPrincipal lenderPrincipal)) {
            throw new IllegalStateException(
                    "No authenticated lender is available");
        }

        return lenderPrincipal;
    }

    public String getLenderId() {
        return get().lenderId();
    }
}
