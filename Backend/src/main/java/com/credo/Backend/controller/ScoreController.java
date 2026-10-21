
package com.credo.backend.controller;

import com.credo.backend.dto.request.ScoreRequest;
import com.credo.backend.dto.response.ScoreResponse;
import com.credo.backend.service.ScoreService;
import jakarta.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/v1")
public class ScoreController {

    private final ScoreService scoreService;

    public ScoreController(ScoreService scoreService) {
        this.scoreService = scoreService;
    }

    @PostMapping("/score")
    public ResponseEntity<List<ScoreResponse>> score(
            @Valid @RequestBody ScoreRequest request) {

        List<ScoreResponse> response = scoreService.score(request);

        return ResponseEntity.ok(response);
    }
}
