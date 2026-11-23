# Pritam Bandgar — Robotics Software Engineering Portfolio

Live website: **https://preetbandgar.github.io/**

A personal engineering portfolio showcasing independent ROS 2 projects, simulation,
autonomous navigation, SLAM, technical case studies, previous experience and research.

## Selected work

- **Autonomous Mobile Robot Navigation & SLAM:** TurtleBot3 mapping, AMCL and Nav2;
  documented doorway experiments and a recorded four-waypoint mission.
- **Differential-Drive Robot Simulation:** Gazebo Harmonic, URDF/Xacro, a 2-DOF arm,
  RGB camera and IMU; configured `robot_localization` EKF, with validation ongoing.
- **Modular ROS 2 Robotics Software Development:** Python (`rclpy`) packages,
  custom ROS interfaces, testing and Docker/GitHub Actions development workflow.
- **ROS 2 Multi-Node Control:** Turtlesim nodes communicating through ROS 2 topics,
  services and custom interfaces.
- **DevOps case studies:** AWS EKS, Terraform, GitHub Actions, Argo CD and Jenkins,
  with original upstream/course sources credited in the respective case studies.

The website also describes MSc dissertation research in computer vision and a
co-authored automated parking systems paper.

## Website technology

Static HTML, CSS and JavaScript deployed with GitHub Pages. The homepage is
assembled from editable `_includes/` sections; project case studies live in
`projects/`. Local images and videos live in `assets/`.

### Preview locally

```bash
python3 -m http.server 8000
```

Open `http://localhost:8000/` in a browser.

### Edit the homepage

Edit the relevant `_includes/*.html` file, then run:

```bash
python3 scripts/build_home.py
```

Commit both the edited include and regenerated `index.html` when publishing.
For the current build process, Python 3 is sufficient; the served website has
no runtime Python requirement.

### Update the CV

Replace `assets/cv/Pritam_Bandgar_CV.pdf` with the current approved PDF while
keeping that filename so existing links continue to work.

## Notes

Project write-ups distinguish completed demonstrations from planned work.
The physical differential-drive robot, Nav2/RTAB-Map integration, and EKF
accuracy validation should be updated as implementation and testing progress.

Maintainer: [Pritam Bandgar](https://github.com/Preetbandgar)
