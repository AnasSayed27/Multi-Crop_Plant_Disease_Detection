# Real-World Field Performance & Optimization Benchmark Log

Official audit trail evaluating model accuracy, confidence, and latency across real-world field photos.

| Timestamp | Milestone / Phase | TTA | Samples | Mean Conf (%) | Mean Latency (ms) |
| :--- | :--- | :---: | :---: | :---: | :---: |
| 2026-08-11 19:59:48 | Step 0 - Baseline (Lab Model) | NO | 10 | 84.69% | 276.6ms |
| 2026-08-11 20:08:46 | Step 0 - Baseline (Lab Model) | NO | 241 | 24.90% | 49.79% | 80.60% | 129.1ms |
| 2026-08-11 20:12:33 | Step 1 - Test-Time Augmentation (TTA) | YES | 241 | 27.39% | 53.53% | 67.17% | 197.7ms |
| 2026-08-11 20:40:39 | Step 2 - Background Removal (rembg) | NO | YES | 241 | 24.48% | 41.08% | 83.94% | 3047.3ms |
| 2026-08-13 12:01:16 | Step 3 - Aggressive Training Augment | NO | NO | 241 | 30.71% | 51.45% | 81.27% | 218.2ms |
| 2026-08-13 12:04:45 | Step 3+TTA - Aggressive Augment + Spatial TTA | YES | NO | 241 | 30.29% | 49.38% | 67.60% | 273.5ms |
