[![License: MIT](https://img.shields.io/badge/License-MIT-maroon.svg)](LICENSE) ![GitHub commit activity](https://img.shields.io/github/commit-activity/t/willegyr/FrameRate?label=Total%20commits&color=%2313A15C) [![Last Commit](https://img.shields.io/github/last-commit/willegyr/MovieLogger?color=orange&label=Last%20Commit)](https://github.com/willegyr/FrameRate/commits/main) [![made-with-python](https://img.shields.io/badge/Language-Python-ffac45.svg?logo=python)](https://python.org) [![Release](https://img.shields.io/badge/Release-v1.0.0-blue)](https://github.com/willegyr/MovieLogger/releases/tag/v1.0.0) ![Repo size](https://img.shields.io/github/repo-size/willegyr/FrameRate) ![Roadmap](https://img.shields.io/badge/Roadmap-In%20Progress-brightgreen)

> ⚠️ **Notice**:  
> This is the README for **version 0.1.0** — the first public pre-release of **FrameRate**.  
> New features and database improvements are planned. Stay tuned on the [Releases page](https://github.com/willegyr/MovieLogger/releases).

# 🎥 FrameRate
*Log, rate, and explore your personal movie database.*

A clean and extensible **Python** project that lets you build your own Letterboxd-style database locally — with movies, actors, ratings, and automatic combined scores.  
Perfect for film enthusiasts who want full control and transparency over their data.

---

## 📜 Table of Contents

- [Features](#features)
- [Preview](#preview)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Database Structure](#database-structure)
- [Roadmap](#roadmap)
- [License](#license)

---

## 🧩 Features

- Log movies with **title, year, director, runtime**, and multiple rating categories.
- Add actors/actresses per movie, including **role name** and **actor-specific rating**.
- Automatic calculation of:
  - 🎞 **Combined movie rating** (weighted mix of your ratings + average actor performance)
  - ⭐ **Combined actor rating** (average across all roles)
- Search functionality for both **movies** and **actors**.
- Top lists:
  - 🏆 Top 10 movies (by combined rating)
  - 🌟 Top 10 actors (by average career rating)
- Fully local — uses **SQLite** with Python’s built-in `sqlite3`.
- Simple text-based menu interface.

---

## 📸 Preview

| Log Movie | Search Movie | Top Lists |
|------------|--------------|-----------|
| <img src="Images/LogMovie.png" width="280" alt="Log Movie Screenshot"> | <img src="Images/SearchMovie.png" width="280" alt="Search Movie Screenshot"> | <img src="Images/TopLists.png" width="280" alt="Top Lists Screenshot"> |

> *(Preview images are optional — you can capture them later when the app runs in your terminal.)*

---

## 🚀 Getting Started

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/willegyr/FrameRate.git
   cd FrameRate

## 🪪 License

This project is licensed under the **MIT License**.  
You’re free to use, modify, and distribute this software — just keep the original license notice.  

See the [LICENSE](LICENSE) file for the full text.
