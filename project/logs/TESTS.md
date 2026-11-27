# Tests

Append new entries at the bottom, with the date. See skill `log-work`.

## 2026-11-05: no robot tests yet
- Reported by the user on 2026-11-05: **the robot has not been built yet**, so none of the robot tests (shots in,
  time between shots, top speed, X-lock push, jams, aim error, calibration, matches, cameras) have been run.
- Only simulation and code results exist: 24 desktop tests pass; the simulated TeleOp scores 3 of 3 for both
  alliances, still and moving (code report, 25 Oct 2026).

## 2026-11-10: robot partly assembled, still no robot tests
- From the team's meeting notes: parts machined and assembly began 19-25 Oct; goBILDA parts arrived and the swerve was
  assembled 26 Oct-1 Nov. The user said on 2026-11-05 that no robot tests can be run yet. Pages now say "not finished"
  instead of "not built".

## 2026-11-11: first robot test results (reported by the user)
- The robot is now built and tested. The user reported these in a message, **without the number of tries, dates or conditions**:
  - Top speed: **250 cm/s** (2.5 m/s).
  - Pushed while in X-lock: **it did not move** (what pushed it, how hard and how many times: not given).
  - Intake: **1 jam**, cleared by reversing the rollers (number of pickups not given).
  - Shots in: **all but 1 from the furthest distance went in** (number of shots and the distances not given).
  - Time between shots: **less than 0.1 s** (how it was measured: not given).
  - Autonomous routes: **"really consistent"** (number of runs not given).
  - Score while still: **3 of 3**. Score while moving: **2 of 3**.
- Compare: the code's `MAX_SPEED` is 2.0 m/s (a simulation setting, so 250 cm/s is not a contradiction but is above it), and the shot logic
  needs aim, speed and hood ready for 0.1 s before it feeds (`Robot.update`), which is worth explaining next to "less than 0.1 s".

## 2026-11-11 (later): facts from the user
- Robot mass **6.5 kg**; the robot holds **4 pollen**; **3 minutes** to swap a pod (reading); the 25 Oct simulation and test results are still current (the
  user: "they are in date"); the team uses odometry for position.

## 2026-11-11 (later): more results (reported by the user)
- Flower mechanism: **empties the flower really well, in under a second** (tries not given).
- Cameras: **both work** on the robot.
- Flywheel: each shot **drops the speed by about 200 encoder ticks** (unit and recovery time not given).
