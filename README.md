# WildMediaServer 🎬

**Stream, Share, Enjoy** - Your Universal Media Server for Cross-Platform Entertainment

[![Build Status](https://img.shields.io/github/actions/workflow/status/Vyx-Software/WildMediaServer/build.yml?style=flat-square&logo=github)](https://github.com/Vyx-Software/WildMediaServer/actions)
[![License](https://img.shields.io/github/license/Vyx-Software/WildMediaServer?style=flat-square&logo=gnu)](LICENSE)
[![Latest Release](https://img.shields.io/github/v/release/Vyx-Software/WildMediaServer?style=flat-square&logo=github)](https://github.com/Vyx-Software/WildMediaServer/releases)

A high-performance media server designed to stream your movies, music, and photos to **any device**, anywhere. Built with cross-platform compatibility and modern streaming standards in mind.

---

## 🚀 Features

- **📺 Multi-Device Streaming**  
  Cast to Smart TVs, game consoles, mobile devices, and browsers simultaneously.
  
- **⚡ On-the-Fly Transcoding**  
  Automatic 4K/HDR/HEVC conversion with hardware acceleration support.

- **🏠 DLNA/UPnP Integration**  
  Seamless compatibility with home theater systems and IoT devices.

- **📡 Live TV & DVR**  
  IPTV support with pause/record functionality (requires compatible tuner).

- **🌐 Modern Web UI**  
  Responsive browser-based interface with dark/light themes.

---

## 📦 Installation

### Native Packages
```bash
# Debian/Ubuntu
wget https://github.com/Vyx-Software/WildMediaServer/releases/download/vX.X.X/wildmediaserver_X.X.X_amd64.deb
sudo dpkg -i wildmediaserver*.deb

# RHEL/CentOS
sudo yum install https://github.com/Vyx-Software/WildMediaServer/releases/download/vX.X.X/wildmediaserver-X.X.X-x86_64.rpm
```

### Docker Deployment
```docker
docker run -d \
  --name wildmediaserver \
  -v /media:/server/media \
  -v /config:/server/config \
  -p 5001:5001 \
  -p 1900:1900/udp \
  --device /dev/dri:/dev/dri \
  vyxsoftware/wildmediaserver:latest
```

### Building from Source
```bash
git clone https://github.com/Vyx-Software/WildMediaServer.git
cd WildMediaServer
mkdir build && cd build
cmake -DCMAKE_BUILD_TYPE=Release ..
make -j$(nproc)
sudo make install
```

---

## 🖥️ Configuration

### Server Settings (`/etc/wildmediaserver.conf`)
```ini
[network]
port = 5001
interface = eth0

[transcoding]
threads = auto
hw_accel = vaapi
max_bitrate = 150M

[library]
auto_scan = true
scan_interval = 3600
```

### Hardware Acceleration
```bash
# Verify VAAPI support
vainfo

# NVIDIA GPU users
docker run ... --runtime=nvidia -e NVIDIA_VISIBLE_DEVICES=all
```

---

## 📱 Supported Protocols & Formats

| Category        | Supported Standards                          |
|-----------------|----------------------------------------------|
| **Video**       | H.264, HEVC, VP9, AV1 (decode)               |
| **Audio**       | FLAC, Opus, Dolby Atmos, DTS-HD MA           |
| **Containers**  | MKV, MP4, TS, WebM                           |
| **Streaming**   | HLS, MPEG-DASH, RTSP, RTP                    |
| **Metadata**    | XML, JSON-LD, embedded tags                  |

---

## 🛠 Development

### Tech Stack
- **Core**: C++20 (ASIO/Boost for networking)
- **Web Interface**: React 18 + TypeScript
- **Media Engine**: FFmpeg 6.x + libav*
- **Packaging**: CPack, Docker, AppImage

### Contribution Workflow
```bash
# Set up development environment
git clone --recurse-submodules https://github.com/Vyx-Software/WildMediaServer.git
cd WildMediaServer
conan install . --output-folder=build --build=missing
cd build && cmake .. -DCMAKE_MODULE_PATH=$(pwd)
cmake --build . --target WildMediaServer
```

---

## 📜 License

```text
GNU GENERAL PUBLIC LICENSE Version 3
Copyright (C) 2023 Vyx-Software

This program comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to redistribute it
under certain conditions. See LICENSE file for details.
```

---

> **Note**  
> For hardware transcoding support, ensure your system meets the  
> [requirements](https://github.com/Vyx-Software/WildMediaServer/wiki/Hardware-Acceleration).  
> 
> Found an issue? [Report it here](https://github.com/Vyx-Software/WildMediaServer/issues/new/choose)  
> Want to contribute? Read our [style guide](CONTRIBUTING.md#code-style) first
