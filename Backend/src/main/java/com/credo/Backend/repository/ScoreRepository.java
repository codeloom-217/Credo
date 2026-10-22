package com.credo.backend.repository;

import com.credo.backend.entity.ScoreRecord;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface ScoreRepository extends JpaRepository<ScoreRecord, Long> {

    List<ScoreRecord> findByCustomerIdOrderByCreatedAtDesc(String customerId);
}