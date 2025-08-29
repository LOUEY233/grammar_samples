# PhysiCell Tumor-Immune Interaction Model

A PhysiCell-based simulation framework for modeling tumor-immune system interactions, with enhanced web-based visualization capabilities.

## 🔬 Overview

This project contains PhysiCell simulations modeling the complex interactions between tumor cells, immune cells (macrophages and CD8 T cells), and their microenvironment. The simulations capture key biological processes including:

- Tumor cell proliferation and oxygen consumption
- Immune cell migration and attack behaviors
- Inflammatory factor secretion and responses  
- Cell death mechanisms (apoptosis, necrosis)
- Debris cleanup by macrophages

## 🚀 Features

### Simulation Models
- **Hypoxia Model**: Tumor cells responding to oxygen gradients
- **Tumor-Immune Model**: Complete tumor-immune system interaction with macrophages and CD8 T cells

### Web Visualization
- Interactive browser-based viewer for simulation results
- Real-time animation playback with speed controls
- Cell type legends with biological explanations
- Responsive design with centered animations

## 📋 Requirements

- **PhysiCell**: Latest version from [PhysiCell.org](http://PhysiCell.MathCancer.org/)
- **C++ Compiler**: gcc or similar
- **Python 3**: For web visualization
- **Modern Web Browser**: For viewing simulations

## 🛠️ Installation & Usage

### 1. Clone Repository
```bash
# Clone this enhanced version:
git clone https://github.com/LOUEY233/grammar_samples.git
cd grammar_samples

# Or clone the original PhysiCell repository:
git clone https://github.com/PhysiCell-Models/grammar_samples.git
cd grammar_samples
```

### 2. Compile and Run Simulation
```bash
# Load tumor-immune model
make load PROJ=tumor_immune_base && make

# Run simulation
./project
```

### 3. View Results with Web Interface
```bash
# Start web viewer
python3 web_viewer.py

# Open in browser
http://localhost:8092
```

## 🎮 Web Viewer Controls

- **Play/Pause**: Spacebar or click button
- **Frame Navigation**: Arrow keys or slider
- **Speed Control**: Dropdown menu (Slow to Very Fast)
- **Cell Information**: Detailed sidebar with cell type descriptions

## 🧬 Cell Types

| Color | Type | Description |
|-------|------|-------------|
| 🔘 Grey | Tumor Cells | Cancer cells that proliferate and consume oxygen |
| 🔴 Red | Macrophages | Immune cells that secrete factors and clean debris |
| 🟡 Yellow | CD8 T Cells | Cytotoxic lymphocytes that attack tumor cells |
| ⚫ Black | Necrotic Cells | Dead cells from oxygen deprivation or immune attack |
| 🟤 Brown | Apoptotic Cells | Cells undergoing programmed death |

## 📁 Project Structure

```
├── config/                 # Configuration files
│   ├── PhysiCell_settings.xml  # Main simulation parameters
│   ├── cell_rules.csv         # Cell behavior rules
│   └── cells.csv              # Initial cell configurations
├── custom_modules/         # Custom PhysiCell modules
│   ├── custom.cpp            # Custom cell behaviors
│   └── custom.h              # Header file
├── web_viewer.py          # Interactive web-based visualization
├── simple_viewer.py       # Backup web viewer
├── main.cpp               # Main simulation entry point
├── Makefile              # Build configuration
└── README.md             # This file
```

## 🔗 Repository Information

- **This Enhanced Fork**: [LOUEY233/grammar_samples](https://github.com/LOUEY233/grammar_samples)
- **Original Repository**: [PhysiCell-Models/grammar_samples](https://github.com/PhysiCell-Models/grammar_samples)
- **Web Visualization**: Enhanced with interactive browser-based viewer
- **Commit History**: Tracked with detailed scientific context

## 🔬 Simulation Parameters

Key parameters can be modified in:
- `config/PhysiCell_settings.xml`: Main simulation settings
- `config/cell_rules.csv`: Cell behavior rules
- Custom modules in `custom_modules/`

## 📊 Output Files

Simulations generate:
- **SVG Files**: Visual snapshots at each time step
- **XML Files**: Detailed cell state data
- **MAT Files**: MATLAB-compatible data exports
- **Graph Files**: Cell interaction networks

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📚 References

- PhysiCell: [http://PhysiCell.MathCancer.org/](http://PhysiCell.MathCancer.org/)
- PhysiCell Documentation: [PhysiCell User Guide](https://github.com/MathCancer/PhysiCell)

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

🔬 Generated with [PhysiCell](http://PhysiCell.MathCancer.org/) | 🌐 Enhanced with Claude Code