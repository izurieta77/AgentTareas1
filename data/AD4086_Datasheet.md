<span id="page-0-0"></span>![](_page_0_Picture_2.jpeg)

# 14-Bit, 40 MSPS, Low Noise, Low Power SAR ADC

#### **FEATURES**

- ► 14-bit resolution, no missing codes
- ► Throughput: 40MSPS, 48.21ns conversion latency
- ► Noise spectral density: 24.18nV/√Hz,158.9dBFS/Hz
- ► Low 1/f, low frequency noise (0.1Hz to 10Hz): 396nV rms
- ► Low Power:85mW typical at 40MSPS
- ► INL: ±12ppm (typ), ±16ppm (max)
- ► Dynamic range: 85.85dBFS
- ► SNR/THD
  - ► 85.34dB (typ)/−110.4dB (typ) at fIN = 1kHz
  - ► 85.27dB (typ)/−101.3dB (typ) at fIN = 1MHz
- ► Easy Drive
  - ► 6V p-p differential input range
  - ► Continuous signal acquisition
  - ► Linearized, 5μA/MSPS input current
- ► Integrated, low-drift reference buffer and decoupling
- ► Integrated VCM generation
- ► Digital features and data interface
  - ► Conversion result FIFO, 16K sample depth
  - ► Digital averaging filter with up to 2<sup>10</sup> decimation
- ► SPI configuration
- ► Configurable data interface
  - ► Single lane, DDR, serial LVDS, 560Mbps per lane
  - ► Dual lane, DDR, serial LVDS, 280Mbps per lane
  - ► Single/quad lane SPI data interface
- ► Package
  - ► [49-ball, 5mm × 5mm CSP\\_BGA, 0.65mm pitch](#page-90-0)
  - ► Integrated supply decoupling capacitors
- ► Operating temperature range: −40°C to +85°C

#### **APPLICATIONS**

- ► Digital imaging
- ► Cell analysis
- ► Spectroscopy
- ► Automated test equipment
- ► High speed data acquisition
- ► Digital control loops, hardware in the loop
- ► Power quality analysis
- ► Source measurement units
- ► Electron and X-ray microscopy
- ► Radar level measurement
- ► Nondestructive test

#### **FUNCTIONAL BLOCK DIAGRAM**

![](_page_0_Figure_46.jpeg)

*Figure 1. AD4086 Functional Block Diagram*

#### **GENERAL DESCRIPTION**

The AD4086 is a high speed, low noise, low distortion, 14-bit, Easy Drive, successive approximation register (SAR) analog-to-digital converter (ADC). Maintaining high performance (signal-to-noise and distortion (SINAD) ratio > 90dBFS) at signal frequencies in excess of 1MHz enables the AD4086 to service a wide variety of precision, wide bandwidth data acquisition applications. Simplification of the input anti-alias filter design can be accomplished by applying oversampling along with the integrated digital filtering and decimation to reduce noise and lower the output data rate for applications that do not require the lowest latency of the AD4086.

The AD4086 Easy Drive features reduce both signal chain complexity and power consumption while enabling greater channel density and flexibility in companion component selection. The product input structure was designed to minimize any input dependent signal currents, therefore reducing any converter induced settling artifacts. The continuous acquisition architecture allows settling across the entire conversion cycle, easing ADC driver settling and bandwidth requirements as compared to other high-speed data converters.

The AD4086 includes several elements that simplify data converter integration: a low drift reference buffer, low dropout (LDO) regulators to generate ADC core and digital interface supply rails, and a 16K result data first-in first out (FIFO) that can greatly reduce the load on the digital host. Additionally, critical supply and reference decoupling capacitors are integrated in the package to ensure optimum performance, simplify printed circuit board (PCB) layout, and reduce the overall solution footprint.

# **TABLE OF CONTENTS**

| Features 1                                    | Applications Information 27            |  |
|-----------------------------------------------|----------------------------------------|--|
| Applications 1                                | Typical Applications Diagrams 27       |  |
| Functional Block Diagram1                     | Analog Front End Design 28             |  |
| General Description1                          | Reference Circuitry Design 29          |  |
| Specifications 3                              | Data Interface Clocking Solution29     |  |
| Timing Specifications 6                       | Power Solution 30                      |  |
| Absolute Maximum Ratings8                     | Digital Interface31                    |  |
| Thermal Resistance 8                          | Overview 31                            |  |
| Electrostatic Discharge (ESD) Ratings8        | ADC Conversion Control31               |  |
| ESD Caution8                                  | SPI Register Interface 31              |  |
| Pin Configuration and Function Descriptions 9 | ADC Conversion Data Interface32        |  |
| Typical Performance Characteristics12         | SPI Configuration Interface 32         |  |
| Terminology 17                                | LVDS Data Interface42                  |  |
| Theory of Operation18                         | SPI Data Interface48                   |  |
| Product Overview18                            | GPIO Pins 49                           |  |
| Converter Operation18                         | Digital Features 51                    |  |
| Transfer Function 19                          | Overview 51                            |  |
| Easy Drive Analog Inputs19                    | Event Detection51                      |  |
| Reference Buffer and Common-Mode Output21     | Result FIFO53                          |  |
| Power Supplies 21                             | Digital Filter 60                      |  |
| Internally Regulated Supply Configuration22   | System Error Correction Coefficients67 |  |
| Externally Generated Supply Configuration 22  | Layout Guidelines68                    |  |
| Power-On Reset (POR) Monitor22                | Configuration Registers69              |  |
| Power Supply Sequence23                       | Register Details71                     |  |
| Power Saving Operating Modes24                | Outline Dimensions 91                  |  |
| Software Reset26                              | Ordering Guide91                       |  |
|                                               |                                        |  |

#### **REVISION HISTORY**

**1/2026—Revision 0: Initial Version**

**[analog.com](http://www.analog.com/en/index.html) Rev. 0 | 2 of 91**

# <span id="page-2-0"></span>**SPECIFICATIONS**

VDD33 = 3.3V ± 5%, VDDLDO = 1.5V to 2.7V, VDD11 = 1.1V ± 5%, IOVDD = 1.1V − 5% to 1.2V + 5%, voltage reference input (VREFIN) = 3.0V, sampling frequency (fS) = 40MHz, and T<sup>A</sup> = TMIN to TMAX, unless otherwise noted.

*Table 1. Specifications*

| Parameter                              | Test Conditions/Comments                                                    | Min             | Typ      | Max             | Unit    |  |
|----------------------------------------|-----------------------------------------------------------------------------|-----------------|----------|-----------------|---------|--|
| RESOLUTION                             |                                                                             | 14              |          |                 | Bits    |  |
| ANALOG INPUT                           |                                                                             |                 |          |                 |         |  |
| Absolute Operating Input Voltage       | Voltage at input, referred to GND                                           | −0.1            |          | VDD33 + 0.1     | V       |  |
| Differential Input Voltage Range       | IN+ voltage − IN− voltage                                                   | −VREFIN         |          | +VREFIN         | V       |  |
| Common-Mode Input Range                |                                                                             | VREFIN/2 − 0.05 | VREFIN/2 | VREFIN/2 + 0.05 | V       |  |
| DC PERFORMANCE                         |                                                                             |                 |          |                 |         |  |
| No Missing Codes                       |                                                                             | 14              |          |                 | Bits    |  |
| Differential Nonlinearity (DNL)        |                                                                             |                 | ±0.063   | ±0.15           | LSB     |  |
| Integral Nonlinearity (INL)            |                                                                             |                 | ±12      | ±16             | ppm     |  |
| Transition Noise                       |                                                                             |                 | 0.3      |                 | LSB rms |  |
| Gain Error                             | TA = 25°C                                                                   |                 | 0.0007   | ±0.045          | %FS     |  |
| Gain Error Drift                       | TA = −40°C to +85°C                                                         |                 | 0.2      |                 | ppm/°C  |  |
| Zero Error                             | TA = 25°C                                                                   |                 | −361     |                 | μV      |  |
| Zero-Error Drift                       | TA = −40°C to +85°C                                                         |                 | 0.05     |                 | ppm/°C  |  |
| Power Supply Rejection                 | VDD33 = 3.3V ± 5%                                                           |                 | −89      |                 | dB      |  |
|                                        | VDD11 = 1.1V ± 5%                                                           |                 | −68      |                 | dB      |  |
| Low Frequency Noise                    | Bandwidth = 0.1Hz to 10Hz                                                   |                 | 396      |                 | nV rms  |  |
| AC PERFORMANCE                         |                                                                             |                 |          |                 |         |  |
| Dynamic Range                          |                                                                             |                 | 85.85    |                 | dB      |  |
| Noise Spectral Density (NSD)           |                                                                             |                 | 158.9    |                 | dBFS/Hz |  |
| Total RMS Noise                        | Bandwidth = 20MHz                                                           |                 | 108.2    |                 | μV rms  |  |
| Signal-to-Noise Ratio (SNR)            | Voltage magnitude (VMAG) = −0.5dBFS, input<br>frequency (fIN) = 1kHz        | 85              | 85.34    |                 | dB      |  |
|                                        | VMAG = −1dBFS, fIN = 1 MHz                                                  |                 | 85.27    |                 | dB      |  |
|                                        | Sinc5 + compensation filter, decimate by 8, VMAG =<br>−0.5dBFS, fIN = 1kHz, | 95.5            | 96.7     |                 | dB      |  |
| Total Harmonic Distortion (THD)        | VMAG = −0.5dBFS, fIN = 1kHz                                                 |                 | −110.4   | −99.2           | dB      |  |
|                                        | VMAG = −1dBFS, fIN = 1MHz                                                   |                 | −101.3   |                 | dB      |  |
| Signal-to-Noise-and-Distortion (SINAD) | VMAG = −0.5dBFS, fIN = 1kHz                                                 |                 | 85.3     |                 | dB      |  |
|                                        | VMAG = −0.5dBFS, fIN = 1MHz                                                 |                 | 85.2     |                 | dB      |  |
| Spurious-Free Dynamic Range            | VMAG = −0.5dBFS, fIN = 1kHz                                                 |                 | 118.7    |                 | dB      |  |
|                                        | VMAG = −0.5dBFS, fIN = 1MHz                                                 |                 | 106.5    |                 | dB      |  |
| −3dB Bandwidth                         | Input at IN+ and IN−, no external filter                                    |                 | 272      |                 | MHz     |  |
| Intermodulation Distortion (IMD)       | Frequency A (fA) = 1.0MHz, Frequency B (fB) =<br>800kHz                     |                 |          |                 |         |  |
| Second-Order IMD (IMD2)                |                                                                             |                 | −93.8    |                 | dB      |  |
| Third-Order IMD (IMD3)                 |                                                                             |                 | −98.7    |                 | dB      |  |
| Power Supply Rejection                 | Ripple voltage = 50mV p-p, f = 1kHz                                         |                 |          |                 |         |  |
| VDD33                                  |                                                                             |                 | −92.5    |                 | dB      |  |
| VDD11                                  |                                                                             |                 | −81.2    |                 | dB      |  |
| REFERENCE INPUT                        |                                                                             |                 |          |                 |         |  |
| VREFIN Range                           |                                                                             | 2.995           | 3.0      | 3.005           | V       |  |
| VREFIN Current                         |                                                                             | −1              |          | 1               | μA/MSPS |  |
|                                        | TA = 25°C                                                                   | −28             |          | 28              | μA      |  |
| VREFIN Leakage Current                 | Converter Idle                                                              | −2              |          | 2               | μA      |  |

**[analog.com](http://www.analog.com/en/index.html) Rev. 0 | 3 of 91**

# **SPECIFICATIONS**

*Table 1. Specifications (Continued)*

| Parameter                                                               | Test Conditions/Comments                                                              | Min           | Typ             | Max          | Unit   |
|-------------------------------------------------------------------------|---------------------------------------------------------------------------------------|---------------|-----------------|--------------|--------|
| COMMON-MODE OUTPUT (CMO)                                                |                                                                                       |               |                 |              |        |
| Absolute Output Voltage                                                 | VREFIN = 3.0V                                                                         | 1.48          |                 | 1.51         | V      |
| Noise                                                                   | Bandwidth = 7.4MHz                                                                    |               | 71              |              | μV rms |
| Noise Spectral Density                                                  |                                                                                       |               | 26.1            |              | nV/√Hz |
| LOW DROPOUT REGULATORS (VDD11, IOVDD)                                   |                                                                                       |               |                 |              |        |
| Input Voltage Range (VDDLDO)                                            |                                                                                       | 1.4           |                 | 2.7          | V      |
| Output Voltage                                                          | TA = 25°C, VDDLDO = 1.8V                                                              |               | 1.1             |              | V      |
| Start-Up Time                                                           |                                                                                       |               | 10              |              | μs     |
| LOW VOLTAGE DIFFERENTIAL SIGNALING<br>(LVDS) INPUT AND OUTPUT (EIA-644) |                                                                                       |               |                 |              |        |
| Data Format                                                             | Serial LVDS data output                                                               |               | Twos complement |              |        |
| LVDS Inputs (CLK± and CNV±)                                             | IOVDD supply domain inputs                                                            |               |                 |              |        |
| Common-Mode Input Voltage (VICM)                                        | Default setting                                                                       | 700           |                 | 1400         | mV     |
| Differential Input Voltage (VIDIFF)                                     | Default setting                                                                       | 100           |                 | 600          | mV     |
| LVDS Outputs (DCO±, DA±, and DB±)                                       | IOVDD supply domain outputs, differential<br>termination, load resistance (RL) = 100Ω |               |                 |              |        |
| Common-Mode Output Voltage (VOCM)                                       | LVDS_VOD = 001b                                                                       | 915           | 927             | 935          | mV     |
|                                                                         | LVDS_VOD = 010b (default)                                                             | 840           | 851             | 860          | mV     |
|                                                                         | LVDS_VOD = 100b                                                                       | 695           | 706             | 715          | mV     |
| Differential Output Voltage (VODIFF)                                    | LVDS_VOD = 001b                                                                       | 370           | 382             | 430          | mV     |
|                                                                         | LVDS_VOD = 010b (default)                                                             | 500           | 510             | 570          | mV     |
|                                                                         | LVDS_VOD = 100b                                                                       | 735           | 745             | 840          | mV     |
| DIGITAL INPUTS (CNV, CS, SCLK, and SDI)                                 | VDD11 supply domain inputs                                                            |               |                 |              |        |
| Input Voltage Tolerance                                                 |                                                                                       | 0             |                 | 2.5          |        |
| Logic Levels                                                            |                                                                                       |               |                 |              |        |
| Input Low Voltage (VIL)                                                 |                                                                                       | 0             |                 | 0.36 × VDD11 |        |
| Input High Voltage (VIH)                                                |                                                                                       | 0.92          |                 | 2.5          |        |
| DIGITAL INPUTS (GPIOx, DCS, and DCLK)                                   | IOVDD supply domain inputs                                                            |               |                 |              |        |
| Input Voltage Tolerance                                                 |                                                                                       | 0             |                 | 1.26         | V      |
| Logic Levels                                                            |                                                                                       |               |                 |              |        |
| VIL                                                                     |                                                                                       | 0             |                 | 0.36 × IOVDD | V      |
| VIH                                                                     |                                                                                       | 0.92          |                 | IOVDD        | V      |
| Input Current                                                           |                                                                                       |               |                 |              |        |
| Input Low Current (IIL)                                                 |                                                                                       | −1            |                 | +1           | μA     |
|                                                                         |                                                                                       | −1            |                 | +1           | μA     |
| Input High Current (IIH)<br>Input Pin Capacitance                       |                                                                                       |               | 4.5             |              | pF     |
|                                                                         |                                                                                       |               |                 |              |        |
| DIGITAL OUTPUTS (GPIOx)<br>Logic Levels                                 | IOVDD supply domain outputs                                                           |               |                 |              |        |
| Output Low Voltage (VOL)                                                | Sink current (ISINK) = 500μA                                                          | 0             |                 | 0.15         | V      |
| Output High Voltage (VOH)                                               | Source current (ISOURCE) = 500μA                                                      | IOVDD − 0.115 |                 | IOVDD        | V      |
| DIGITAL OUTPUTS (SDOx)                                                  | IOVDD supply domain outputs.                                                          |               |                 |              |        |
| Data Format                                                             | Configured as serial data output                                                      |               | Twos complement |              |        |
| Logic Levels                                                            |                                                                                       |               |                 |              |        |
|                                                                         |                                                                                       |               |                 |              |        |
| VOL                                                                     | ISINK = 500μA                                                                         | 0             |                 | 0.15         | V      |

**[analog.com](http://www.analog.com/en/index.html) Rev. 0 | 4 of 91**

# **SPECIFICATIONS**

*Table 1. Specifications (Continued)*

| Parameter             | Test Conditions/Comments                    | Min   | Typ  | Max   | Unit |  |
|-----------------------|---------------------------------------------|-------|------|-------|------|--|
| POWER SUPPLIES        |                                             |       |      |       |      |  |
| VDD33                 |                                             | 3.135 | 3.30 | 3.465 | V    |  |
| VDDLDO                |                                             | 1.4   |      | 2.7   | V    |  |
| VDD11                 | Applied externally, LDO disabled            | 1.045 | 1.10 | 1.155 | V    |  |
| IOVDD                 | Applied externally, LDO disabled            | 1.045 | 1.10 | 1.26  | V    |  |
| Operating Current     | LVDS_CNV_EN = 0                             |       |      |       |      |  |
| Static                | Converter and interface idle, FIFO disabled |       |      |       |      |  |
| VDD33                 |                                             |       | 5.72 | 7.14  | mA   |  |
| VDDLDO                | VDD11 LDO disabled                          |       | 0    | 0.02  | mA   |  |
| VDD11                 |                                             |       | 16.4 | 23    | mA   |  |
| IOVDD                 |                                             |       | 5.43 | 6     | mA   |  |
| VDDLDO                | VDD11 LDO enabled                           |       | 21.5 | 26.5  | mA   |  |
| Dynamic               | DC input signal                             |       |      |       |      |  |
| VDD33                 |                                             |       | 16.4 | 18.72 | mA   |  |
| VDDLDO                | VDD11 LDO disabled                          |       | 0    | 0.02  | mA   |  |
| VDD11                 |                                             |       | 24.5 | 30.8  | mA   |  |
| IOVDD                 |                                             |       | 8.3  | 9.3   | mA   |  |
| VDDLDO                | VDD11 LDO enabled                           |       | 30.9 | 36.8  | mA   |  |
| Dynamic               | −0.5dBFS sine-wave input signal             |       |      |       |      |  |
| VDD33                 |                                             |       | 14.7 | 16.2  | mA   |  |
| VDDLDO                | VDD11 LDO disabled                          |       | 0    | 0.02  | mA   |  |
| VDD11                 |                                             |       | 24.5 | 31    | mA   |  |
| IOVDD                 |                                             |       | 8.7  | 9.8   | mA   |  |
| VDDLDO                | VDD11 LDO enabled                           |       | 31   | 37    | mA   |  |
| Standby Mode          | LVDS_SELF_CLK_MODE disabled                 |       |      |       |      |  |
| VDD33                 |                                             |       | 1.4  | 1.9   | mA   |  |
| VDDLDO                | VDD11 LDO disabled                          |       | 0    | 0.02  | mA   |  |
| VDD11                 |                                             |       | 1.7  | 5.1   | mA   |  |
| IOVDD                 |                                             |       | 62   | 376   | µA   |  |
| VDDLDO                | VDD11 LDO enabled                           |       | 1.7  | 4.8   | mA   |  |
| Sleep Mode            | LVDS_SELF_CLK_MODE disabled                 |       |      |       |      |  |
| VDD33                 |                                             |       | 0.6  | 0.9   | mA   |  |
| VDDLDO                | VDD11 LDO disabled                          |       | 0    | 0.02  | mA   |  |
| VDD11                 |                                             |       | 1.7  | 4.4   | mA   |  |
| IOVDD                 |                                             |       | 62   | 375   | µA   |  |
| VDDLDO                | VDD11 LDO enabled                           |       | 1.4  | 4.5   | mA   |  |
| Power Dissipation     |                                             |       |      |       |      |  |
| Static                | VDD11 LDO disabled                          |       | 42.9 | 58.9  | mW   |  |
| Dynamic               | DC input signal                             |       | 90.2 | 112.2 | mW   |  |
| Dynamic               | −0.5dBFS sine-wave input signal             |       | 85   | 104.3 | mW   |  |
| Standby Mode          | VDD11 LDO disabled                          |       | 6.6  | 12.9  | mW   |  |
| Sleep Mode            | VDD11 LDO disabled                          |       | 3.9  | 8.7   | mW   |  |
| TEMPERATURE RANGE     |                                             |       |      |       |      |  |
| Specified Performance | TMIN to TMAX                                | −40   |      | +85   | °C   |  |

**[analog.com](http://www.analog.com/en/index.html) Rev. 0 | 5 of 91**

# <span id="page-5-0"></span>**SPECIFICATIONS**

### **TIMING SPECIFICATIONS**

VDD33 = 3.3V ± 5%, VDDLDO= 1.5V to 2.7V, VDD11 = 1.1V ± 5%, IOVDD = 1.1V − 5% to 1.2V + 5%, VREFIN = 3.0V, f<sup>S</sup> = 40MHz, and T<sup>A</sup> = TMIN to TMAX, unless otherwise noted.

*Table 2. Timing Specifications*

| Parameter                                                        | Symbol   | Min         | Typ                         | Max          | Unit |
|------------------------------------------------------------------|----------|-------------|-----------------------------|--------------|------|
| Sampling Frequency                                               | fS       | 1.25        |                             | 40           | MHz  |
| Conversion Time                                                  | tCONV    | 25          |                             | 800          | ns   |
| Acquisition Phase                                                | tACQ     | tCYC        |                             |              | ns   |
| Conversion Cycle Period                                          | tCYC     | tCONV       |                             |              | ns   |
| LVDS Data Interface                                              |          |             |                             |              |      |
| Data Interface Clock Count                                       | N        |             |                             | 7            |      |
| Active Data Lane Count                                           | L        |             |                             | 2            |      |
| CNV± High Time                                                   | tCNVH    | tCLK        | 4 × tCLK                    | tCYC − tCNVL | ns   |
| CNV± Low Time                                                    | tCNVL    | tCLK        | 4 × tCLK                    | tCYC − tCNVH | ns   |
| CNV± Edge to CLK± Rising Edge Alignment                          | tCCA     |             |                             | 535          | ps   |
| CNV± to Dx± (MSB) Ready                                          | tMSB     |             |                             |              |      |
| Gain Error Correction Enabled                                    |          |             | 20.5                        | 22.4         | ns   |
| Gain Error Correction Disabled                                   |          |             | 15.7                        | 18           | ns   |
| CLK± Period                                                      | tCLK     | 3.571       |                             | tCYC × L/N   | ns   |
| CLK± Frequency                                                   | fCLK     |             | 1/tCLK                      | 280          | MHz  |
| CLK± to Dx± Delay                                                | tCLKD    | 1           |                             | 2.1          | ns   |
| CLK± to DCO± Delay (Echo Clock Mode)                             | tDCO     | 1           |                             | 2            | ns   |
| DCO± to Dx± Delay (Echo Clock Mode)                              | tDCOD    | 0.02        |                             | 1            | ns   |
| Serial Peripheral Interface (SPI) Data Interface                 |          |             |                             |              |      |
| Data Interface Clock Count, Single Conversion Result             | M        |             |                             | 24           |      |
| Active Data Lane Count                                           | C        |             | 1                           | 4            |      |
| Data Interface Chip Select Falling Edge (DCS) to SDOB Data Valid | tDEN     | 5           | 6                           |              | ns   |
| Data Interface Clock Period (DCLK)                               | tDCK     | 20          |                             |              | ns   |
| Data Interface Clock Low Pulse Width (DCLK)                      | tDCKL    | tDCK × 0.45 |                             |              | ns   |
| Data Interface Clock High Pulse Width (DCLK)                     | tDCLKH   | tDCK × 0.45 |                             |              | ns   |
| Data Interface Clock Falling Edge to Data Remains Valid Delay    | tDHSDO   | 5           |                             |              | ns   |
| Data Interface Clock Falling Edge to Data Valid Delay            | tDDSDO   |             |                             | 9.6          | ns   |
| DCLK Rising to Data Interface Chip Select Falling                | tDCKEN   | 0           |                             |              | ns   |
| Data Interface Chip Select High to DCLK Disabled                 | tDCLKDIS | 0           |                             |              | ns   |
| Data Interface Chip Select High Between Frames                   | tDCSMIN  |             | (tDCKEN + tDCLKDIS) + 0.5 × |              | ns   |
|                                                                  |          |             | tDCLK                       |              |      |
| Serial Configuration Interface                                   |          |             |                             |              |      |
| SCLK Period                                                      | tSCK     | 20          |                             |              | ns   |
| SCLK Low Pulse Width                                             | tSCKL    | tSCK × 0.45 |                             |              | ns   |
| SCLK High Pulse Width                                            | tSCKH    | tSCK × 0.45 |                             |              | ns   |
| SCLK Falling Edge to Data Remains Valid Delay                    | tHSDO    | 0.7         |                             |              | ns   |
| SCLK Falling Edge to Data Valid Delay                            | tDSDO    |             |                             | 14.5         | ns   |
| CS Falling Edge to SCLK                                          | tCSSCK   | 0           |                             |              | ns   |
| Last SCLK to CS Rising                                           | tSCKCS   | 0           |                             |              | ns   |
| SDI Valid Setup Time Before SCLK Rising Edge                     | tSSDI    | 1           |                             |              | ns   |
| SDI Valid Hold Time After SCLK Rising Edge                       | tHSDI    | 0           |                             |              | ns   |
| SCLK Rising to Data Interface Chip Select Falling                | tSCKEN   | 0           |                             |              | ns   |

**[analog.com](http://www.analog.com/en/index.html) Rev. 0 | 6 of 91**

# **SPECIFICATIONS**

*Table 2. Timing Specifications (Continued)*

| Parameter                                        | Symbol    | Min      | Typ                             | Max      | Unit |
|--------------------------------------------------|-----------|----------|---------------------------------|----------|------|
| Data Interface Chip Select High to SCLK Disabled | tSCKDIS   | 0        |                                 |          | ns   |
| Data Interface Chip Select High to SDO Disabled  | tCSDIS    |          |                                 | 10.3     | ns   |
| Data Interface Chip Select High Between Frames   | tCSMIN    |          | (tSCKEN + tSCKDIS) + 0.5 × tSCK |          | ns   |
| Digital Filter                                   |           |          |                                 |          |      |
| FILT_SYNC Rising Edge to CNV Rising Edge         | tSYNC MAX |          | tCYC − 5                        |          | ns   |
| CNV Rising Edge to FILT_SYNC Falling Edge        | tSYNC MIN |          | 3                               |          | ns   |
| Event Detection                                  |           |          |                                 |          |      |
| Input Threshold Crossed to ALERT Asserted        | tEVT      | 2 × tCYC |                                 | 3 × tCYC |      |

**[analog.com](http://www.analog.com/en/index.html) Rev. 0 | 7 of 91**

# <span id="page-7-0"></span>**ABSOLUTE MAXIMUM RATINGS**

*Table 3. Absolute Maximum Ratings*

| Parameter                                          | Rating          |
|----------------------------------------------------|-----------------|
| Analog Inputs                                      |                 |
| IN+, AUXIN+, IN−, and AUXIN− to GND                | −0.3V to +3.6V  |
| Analog Output                                      |                 |
| CMO                                                | −0.3V to +3.6V  |
| Supply Voltage                                     |                 |
| REFIN and VDD33 to GND                             | −0.3V to +3.6V  |
| VDDLDO to GND                                      | −0.3V to +2.75V |
| VDD11 to GND                                       | −0.3V to +1.26V |
| IOVDD to GND                                       | −0.3V to +1.26V |
| Digital Inputs and Outputs                         |                 |
| Inputs (CNV± and CLK±) to GND                      | −0.3V to +2.75V |
| LVDS OUTPUT (DCO±, DA±, and DB±) to GND            | −0.3V to +1.26V |
| CS, SCLK, and SDI to GND                           | −0.3V to +2.75V |
| GPIO0, GPIO1, GPIO2, and GPIO3 to GND              | −0.3V to +1.26V |
| Temperature                                        |                 |
| Storage Range                                      | −55°C to +150°C |
| Operating Range                                    | −40°C to +85°C  |
| Maximum Reflow (Package) as per<br>JEDEC J-STD-020 | 260°C           |

Stresses at or above those listed under Absolute Maximum Ratings may cause permanent damage to the product. This is a stress rating only; functional operation of the product at these or any other conditions above those indicated in the operational section of this specification is not implied. Operation beyond the maximum operating conditions for extended periods may affect product reliability.

# **THERMAL RESISTANCE**

Thermal performance is directly linked to PCB design and operating environment. Careful attention to PCB thermal design is required.

*Table 4. Thermal Resistance*

| Package<br>Type | θJA1 | ΨJT1 | ΨJB1 | θJB2 | θJC3 | Unit |
|-----------------|------|------|------|------|------|------|
| BC-49-8         | 66.8 | 1.7  | 45.1 | 45.9 | 53.1 | °C/W |

- <sup>1</sup> <sup>θ</sup>JA, ΨJT, and ΨJB are modeled using a JEDEC 2S2P test PCB with 16 thermal vias, in a JEDEC natural convection environment.
- <sup>2</sup> <sup>θ</sup>JB is modeled using a JEDEC 2S2P test PCB with 16 thermal vias, in a JEDEC junction to board environment.
- <sup>3</sup> <sup>θ</sup>JC is modeled using a JEDEC 1S test PCB, with an infinite heatsink attached directly to the package surface.

### **ELECTROSTATIC DISCHARGE (ESD) RATINGS**

The following ESD information is provided for handling of ESD-sensitive devices in an ESD-protected area only.

Human body model (HBM) per ANSI/ESDA/JEDEC JS-001.

Field induced charged-device model (FICDM) per ANSI/ESDA/JE-DEC JS-002.

# **ESD Ratings for the AD4086**

*Table 5. AD4086, 49-Ball CSP\_BGA*

| ESD Model                                                                                   | Withstand Threshold (V) | Class |
|---------------------------------------------------------------------------------------------|-------------------------|-------|
| HBM (Pin E1, Pin E2, Pin D1, and Pin<br>D2 (IN−, AUXIN−, IN+, and AUXIN+,<br>respectively)) | 1000                    | 1C    |
| HBM (All other pins)                                                                        | 1500                    | 1C    |
| FICDM                                                                                       | 750                     | C2b   |

#### **ESD CAUTION**

![](_page_7_Picture_20.jpeg)

**ESD (electrostatic discharge) sensitive device**. Charged devices and circuit boards can discharge without detection. Although this product features patented or proprietary protection circuitry, damage may occur on devices subjected to high energy ESD. Therefore, proper ESD precautions should be taken to avoid performance degradation or loss of functionality.

**[analog.com](http://www.analog.com/en/index.html) Rev. 0 | 8 of 91**

# <span id="page-8-0"></span>**PIN CONFIGURATION AND FUNCTION DESCRIPTIONS**

![](_page_8_Figure_2.jpeg)

*Figure 2. Pin Configuration*

*Table 6. Pin Function Descriptions*

| Pin No.                       | Mnemonic   | Type1 | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
|-------------------------------|------------|-------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| A1, A2, A3                    | VDD11      | P     | 1.1V ADC Core Supplies. These supply pins are internally decoupled by four 470nF<br>capacitors to GND.                                                                                                                                                                                                                                                                                                                                                                                                                   |
|                               |            |       | When power is supplied to VDDLDO (B3), an internal LDO voltage regulator produces<br>the 1.1V required at these pins. The voltage regulator is automatically powered on<br>when VDDLDO is greater than 1.4V.                                                                                                                                                                                                                                                                                                             |
|                               |            |       | If VDDLDO is left disconnected, the required 1.1V must be supplied to these pins from<br>an external source.                                                                                                                                                                                                                                                                                                                                                                                                             |
| A4, A5                        | CNV+, CNV− | DI    | Convert Start Inputs. This pin pair serves as the conversion control input. A conversion<br>is initiated on the rising edge of the convert signal.                                                                                                                                                                                                                                                                                                                                                                       |
|                               |            |       | These inputs are, by default, configured in complementary metal-oxide semiconductor<br>(CMOS) mode, in which CNV− must be tied to IOGND, and the convert signal is<br>applied to CNV+. In the LVDS data interface mode, the convert start input can be<br>optionally configured in LVDS mode, in which case, the convert signal is applied<br>differentially to CNV+ and CNV− and an external 100Ω termination resistor must be<br>placed across these pins. See the ADC Conversion Control section for further details. |
| A6                            | IOVDD      | P     | 1.1V Digital Interface Supply Rail. This supply is internally decoupled by a 220nF<br>capacitor to IOGND.                                                                                                                                                                                                                                                                                                                                                                                                                |
|                               |            |       | When power is supplied to VDDLDO (B3), an internal LDO voltage regulator produces<br>the 1.1V required at this pin. The voltage regulator is automatically powered on when<br>VDDLDO is greater than 1.5V.                                                                                                                                                                                                                                                                                                               |
|                               |            |       | If VDDLDO is left disconnected, the required 1.1V must be supplied to this pin from an<br>external source (typically the host controller interface supply).                                                                                                                                                                                                                                                                                                                                                              |
| A7                            | CLK−/DCS   | DI    | Data Interface Clock Input (CLK−)/Data Interface Chip Select (DCS) Multifunction Pin.                                                                                                                                                                                                                                                                                                                                                                                                                                    |
|                               |            |       | In LVDS data interface mode (default), this pin serves as half of the differential data<br>clock input, and an external 100Ω termination resistor must be present between it and<br>the CLK+ pin.                                                                                                                                                                                                                                                                                                                        |
|                               |            |       | In SPI data interface mode, this pin functions as a chip select input (data interface chip<br>select).                                                                                                                                                                                                                                                                                                                                                                                                                   |
| B1, B2, C1, C2, F5,<br>F6, G5 | REFGND     | P     | Reference Grounds. Connect any external reference decoupling capacitors across<br>REFIN and REFGND. REFGND must be tied with a low impedance path to GND.                                                                                                                                                                                                                                                                                                                                                                |
| B3                            | VDDLDO     | P     | LDO Supply Rail Input.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
|                               |            |       | This supply rail is internally decoupled by a 220nF capacitor to GND. The two internal<br>1.1V LDO voltage regulators can be supplied from a source connected to this input<br>in the 1.5V to 2.7V range. If this pin is left open, the internal regulators automatically                                                                                                                                                                                                                                                |

**[analog.com](http://www.analog.com/en/index.html) Rev. 0 | 9 of 91**

# **PIN CONFIGURATION AND FUNCTION DESCRIPTIONS**

*Table 6. Pin Function Descriptions (Continued)*

| Pin No.                         | Mnemonic   | Type1 | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
|---------------------------------|------------|-------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|                                 |            |       | power off, and both VDD11and IOVDD must be connected with an external voltage                                                                                                                                                                                                                                                                                                                                                                                   |
|                                 |            |       | source within their allowed specification limits.                                                                                                                                                                                                                                                                                                                                                                                                               |
|                                 |            |       | If VDDLDO is connected to a voltage source, neither VDD11 nor IOVDD should be                                                                                                                                                                                                                                                                                                                                                                                   |
|                                 |            |       | connected to any external voltage source.                                                                                                                                                                                                                                                                                                                                                                                                                       |
| B4, B5                          | DCO−, DCO+ | DO    | LVDS Echo Clock Outputs.                                                                                                                                                                                                                                                                                                                                                                                                                                        |
|                                 |            |       | In LVDS data interface mode (default), this pin pair outputs a buffered and delayed<br>version of CLK+ and CLK−. Data outputs from LVDS Data Lane DA+ and Data Lane<br>DA− (and Data Lane DB+ and Data Lane DB− if active) are clocked out in alignment<br>with both rising and falling edges of DCO+ and DCO−. In SPI data interface mode (or<br>if the echo clock mode is disabled while in LVDS data interface mode), these pins can<br>be left unconnected. |
| B6                              | IOGND      | P     | Digital Interface Supply Ground Reference. This pin must be connected to the same<br>ground plane as all other GND pins.                                                                                                                                                                                                                                                                                                                                        |
|                                 |            |       | All pins specified as type DI, DO, or DI/O must use this ground reference.                                                                                                                                                                                                                                                                                                                                                                                      |
| B7                              | CLK+/DCLK  | DI    | Data Interface Clock Input Multifunction Pin.                                                                                                                                                                                                                                                                                                                                                                                                                   |
|                                 |            |       | In LVDS data interface mode (default), this pin serves as half of the differential data                                                                                                                                                                                                                                                                                                                                                                         |
|                                 |            |       | clock input, and an external 100Ω termination resistor must be present between it and<br>the CLK− pin.                                                                                                                                                                                                                                                                                                                                                          |
|                                 |            |       | In SPI data interface mode, the single-ended data clock signal must be applied to this<br>pin.                                                                                                                                                                                                                                                                                                                                                                  |
| C3 to C5, D3 to D5,<br>E3 to E5 | GND        | P     | Grounds. All ground pins must be connected to a PCB GND plane.                                                                                                                                                                                                                                                                                                                                                                                                  |
| C6                              | DB+/SDOC   | DO    | Data Interface Output Multifunction Pin.                                                                                                                                                                                                                                                                                                                                                                                                                        |
|                                 |            |       | In LVDS data interface mode (default), this output pin along with DB− serves as the<br>optional, secondary LVDS Data Lane B. If unused, leave unconnected.                                                                                                                                                                                                                                                                                                      |
|                                 |            |       | In SPI data interface mode, this pin functions as Serial Data Output C (SDOC), which<br>is active in a four-lane configuration only. Result data is shifted out of this pin on the<br>falling edge of the data interface clock (DCLK).                                                                                                                                                                                                                          |
|                                 |            |       | This pin must left unconnected if not being used.                                                                                                                                                                                                                                                                                                                                                                                                               |
| C7                              | DA+/SDOA   | DO    | Data Interface Output Multifunction Pin.                                                                                                                                                                                                                                                                                                                                                                                                                        |
|                                 |            |       | In LVDS data interface mode (default), this output pin along with DA− serves as the<br>primary LVDS Data Lane A.                                                                                                                                                                                                                                                                                                                                                |
|                                 |            |       | In SPI data interface mode, this pin functions as Serial Data Output A (SDOA), which<br>is active in a four-lane configuration only. Result data is shifted out of this pin on the<br>falling edge of the data interface clock (DCLK).                                                                                                                                                                                                                          |
|                                 |            |       | This pin must left unconnected if not being used.                                                                                                                                                                                                                                                                                                                                                                                                               |
| D1                              | IN+        | AI    | Positive Analog Differential Input.                                                                                                                                                                                                                                                                                                                                                                                                                             |
| D2                              | AUXIN+     | AI    | Positive Auxiliary Analog Differential Input.                                                                                                                                                                                                                                                                                                                                                                                                                   |
| D6                              | DB−/SDOD   | DO    | Data Interface Output Multifunction Pin.                                                                                                                                                                                                                                                                                                                                                                                                                        |
|                                 |            |       | In LVDS data interface mode (default), this output pin along with DB+ serves as the<br>optional, secondary LVDS Data Lane B. If unused, leave unconnected.                                                                                                                                                                                                                                                                                                      |
|                                 |            |       | In SPI data interface mode, this pin functions as Serial Data Output D (SDOD), which<br>is active in a four-lane configuration only. Result data is shifted out of this pin on the<br>falling edge of the data interface clock (DCLK). Note that this pin does not go into a<br>high-impedance state when used in four-lane SPI mode when CS is inactive.                                                                                                       |
|                                 |            |       | This pin must be left unconnected if not being used.                                                                                                                                                                                                                                                                                                                                                                                                            |
| D7                              | DA−/SDOB   | DO    | Data Interface Output.                                                                                                                                                                                                                                                                                                                                                                                                                                          |
|                                 |            |       | In LVDS data interface mode (default), this output pin along with DA+ serves as the                                                                                                                                                                                                                                                                                                                                                                             |
|                                 |            |       | primary LVDS Data Lane A. If unused, leave unconnected.                                                                                                                                                                                                                                                                                                                                                                                                         |
|                                 |            |       | In SPI data interface mode, this pin functions as Serial Data Output B (SDOB). This is<br>the only active serial data output in single lane mode. Result data is shifted out of this<br>pin on the falling edge of the data interface clock (DCLK).                                                                                                                                                                                                             |

**[analog.com](http://www.analog.com/en/index.html) Rev. 0 | 10 of 91**

# <span id="page-10-0"></span>**PIN CONFIGURATION AND FUNCTION DESCRIPTIONS**

*Table 6. Pin Function Descriptions (Continued)*

| Pin No. | Mnemonic | Type1 | Description                                                                                                                           |
|---------|----------|-------|---------------------------------------------------------------------------------------------------------------------------------------|
| E1      | IN−      | AI    | Negative Analog Differential Input.                                                                                                   |
| E2      | AUXIN−   | AI    | Negative Auxiliary Analog Differential Input.                                                                                         |
| E6      | GPIO1    | DI/O  | General-Purpose Input and Output 1 Pin.                                                                                               |
| E7      | SCLK     | DI    | Configuration Interface Serial Data Clock. This clock input is used to shift data into and<br>out of the device configuration memory. |
| F1      | GPIO2    | DI/O  | General-Purpose Input and Output 2 Pin.                                                                                               |
| F2      | GPIO3    | DI/O  | General-Purpose Input and Output 3 Pin.                                                                                               |
| F3, G3  | VDD33    | P     | 3.3V Supply Rail Inputs. These supply pins are internally decoupled by a 470nF<br>capacitor to GND.                                   |
| F4, G4  | REFIN    | AI    | 3.0V Reference Voltage Inputs.                                                                                                        |
| F7      | SDI      | DI    | Serial Data Input. Configuration data is shifted into this input on the rising edge of the<br>serial data clock, SCLK.                |
| G1      | CS       | DI    | Configuration Interface Chip Select Input (Active Low). The CS input frames serial<br>data transfers over the configuration SPI.      |
| G2      | CMO      | AO    | Common-Mode Voltage (VCM) Output.                                                                                                     |
| G6      | DNC      | DNC   | Do Not Connect.                                                                                                                       |
| G7      | GPIO0    | DI/O  | General-Purpose Input and Output 0 Pin. This is default configured as Configuration<br>SPI SDO Data.                                  |

<sup>1</sup> AI is analog input, AO is analog output, DI is digital input, DI/O is digital input and output, DO is digital output, and P is power.

**[analog.com](http://www.analog.com/en/index.html) Rev. 0 | 11 of 91**

#### <span id="page-11-0"></span>**TYPICAL PERFORMANCE CHARACTERISTICS**

![](_page_11_Figure_2.jpeg)

*Figure 3. Fast Fourier Transform (FFT) 40MSPS, fIN = 1kHz, −0.5dBFS*

![](_page_11_Figure_4.jpeg)

*Figure 4. FFT 40MSPS, fIN = 1MHz, −1.0dBFS*

![](_page_11_Figure_6.jpeg)

*Figure 5. SNR vs. Input Signal Frequency (Amplitude = −0.5dBFS, −1dBFS, −3dBFS, −6dBFS, −10dBFS, and −12dBFS)*

![](_page_11_Figure_8.jpeg)

*Figure 6. THD vs. Input Signal Frequency (Amplitude = −0.5dBFS, −1dBFS, −3dBFS, −6dBFS, −10dBFS, and −12dBFS)*

![](_page_11_Figure_10.jpeg)

*Figure 7. Small Signal −3dB Bandwidth at 40MSPS*

![](_page_11_Figure_12.jpeg)

*Figure 8. Sinc5 + Compensation Filter, Pass-Band Flatness*

**[analog.com](http://www.analog.com/en/index.html) Rev. 0 | 12 of 91**

#### **TYPICAL PERFORMANCE CHARACTERISTICS**

![](_page_12_Figure_2.jpeg)

*Figure 9. Sinc1 Filter Response, f<sup>S</sup> = 40MHz (DEC × Means Decimate By)*

![](_page_12_Figure_4.jpeg)

*Figure 10. Sinc5 Filter Response, f<sup>S</sup> = 40MHz*

![](_page_12_Figure_6.jpeg)

*Figure 11. Sinc5 + Compensation Filter Response, f<sup>S</sup> = 40MHz*

![](_page_12_Figure_8.jpeg)

*Figure 12. SNR vs. Total Decimation Factor*

![](_page_12_Figure_10.jpeg)

*Figure 13. DNL vs. Code for Various Temperatures, 40MSPS*

![](_page_12_Figure_12.jpeg)

*Figure 14. INL vs. Code for Various Temperatures, 40MSPS*

**[analog.com](http://www.analog.com/en/index.html) Rev. 0 | 13 of 91**

# **TYPICAL PERFORMANCE CHARACTERISTICS**

![](_page_13_Figure_2.jpeg)

*Figure 15. Low Frequency Noise, Inputs Shorted*

![](_page_13_Figure_4.jpeg)

*Figure 16. Histogram of Codes, Sinc1, No Filter, Decimate 2×, Decimate 4× … Decimate 1024×*

![](_page_13_Figure_6.jpeg)

*Figure 17. Histogram of Codes, Sinc5, No Filter, Decimate 2×, Decimate 4× ...Decimate 256×*

![](_page_13_Figure_8.jpeg)

*Figure 18. Histogram of Codes, Sinc5 + Compensation, No Filter, Decimate 2×, Decimate 4× … Decimate 512×*

![](_page_13_Figure_10.jpeg)

*Figure 19. Offset Voltage Histogram*

![](_page_13_Figure_12.jpeg)

*Figure 20. Offset Drift vs. Temperature*

**[analog.com](http://www.analog.com/en/index.html) Rev. 0 | 14 of 91**

#### <span id="page-14-0"></span>**TYPICAL PERFORMANCE CHARACTERISTICS**

![](_page_14_Figure_2.jpeg)

*Figure 21. Gain Error vs. Temperature*

![](_page_14_Figure_4.jpeg)

*Figure 22. PSRR vs. Frequency*

![](_page_14_Figure_6.jpeg)

*Figure 23. CMO Voltage vs. Temperature*

![](_page_14_Figure_8.jpeg)

*Figure 24. CMO Voltage Variation vs. Load Resistance*

![](_page_14_Figure_10.jpeg)

*Figure 25. Dynamic REFIN Current vs. Temperature*

![](_page_14_Figure_12.jpeg)

*Figure 26. Total Power vs. Sampling Frequency*

**[analog.com](http://www.analog.com/en/index.html) Rev. 0 | 15 of 91**

# **TYPICAL PERFORMANCE CHARACTERISTICS**

![](_page_15_Figure_2.jpeg)

*Figure 27. Total Power at 40MSPS vs. Temperature*

![](_page_15_Figure_4.jpeg)

*Figure 28. Total Power vs. Temperature in Sleep and Standby Modes*

![](_page_15_Figure_6.jpeg)

*Figure 29. AC CMMR vs. Input Frequency*

**[analog.com](http://www.analog.com/en/index.html) Rev. 0 | 16 of 91**

### <span id="page-16-0"></span>**TERMINOLOGY**

#### **Integral Nonlinearity Error (INL)**

INL refers to the deviation of each output code from a line drawn between points at negative full scale and positive full scale. The negative full-scale reference is defined by an input level equivalent to ½ LSB prior to the first code transition. The positive full-scale reference is defined as an input level that is 1½ LSB beyond the last code transition. The deviation is measured from the center of each code relative to the straight line.

# **Differential Nonlinearity Error (DNL)**

In an ideal ADC, code transitions occur at 1 LSB intervals. DNL is a measure of the maximum deviation of any code from the ideal code width. DNL is specified in terms of resolution for which no missing codes are guaranteed.

#### **Zero Error**

Zero error is the difference between the ideal midscale voltage, 0V, and the applied voltage producing the midscale output code, 0LSB.

### **Gain Error**

Gain error is specified as the difference in the slope of the ADC transfer characteristic vs. that of an ideal converter. In an ideal data converter, the first code transition (100 … 00 to 100 … 01) occurs ½ LSB more than the nominal negative full-scale input (−2.999997V for a ±3.0V range at 14 bits) and the last code transition (011 … 10 to 011 … 11) occurs 1½ LSB less than the nominal positive full-scale input (+2.999991V for a ±3.0V range at 14 bits).

# **Reference Voltage Buffer Temperature Coefficient**

[Remove this section]

#### **Aperture Delay**

[Please remove this section]

#### **Transient Response**

[Please remove section]

#### **Signal-to-Noise Ratio (SNR)**

SNR is the computed ratio of the fundamental signal amplitude measured in RMS volts and the root sum of squares of all other spectral components in the Nyquist bandwidth (f < fS/2) excluding harmonics and DC components. The computed value of SNR is converted into a logarithmic scale and expressed in decibels (dB).

#### **Signal-to-Noise-and-Distortion (SINAD) Ratio**

SINAD is the computed ratio of the fundamental signal amplitude measured in RMS volts and the root sum of squares of all other spectral components in the Nyquist bandwidth (f < fS/2) including harmonic components but excluding the DC component. The computed value of SINAD is converted into a logarithmic scale and expressed in decibels (dB).

#### **Total Harmonic Distortion (THD)**

THD is the ratio of the RMS sum of the amplitudes of the first five harmonic components to the RMS amplitude of a full-scale input signal expressed in decibels (dB).

### **Effective Number of Bits (ENOB)**

ENOB is a measure of the effective resolution of the data converter in the presence of a sinusoidal input signal. ENOB can be computed from SINAD using the following equation and is expressed in bits:

ENOB = (SINADdB – 1.76)/6.02

#### **Spurious-Free Dynamic Range (SFDR)**

SFDR is the ratio between the RMS amplitude of the input signal and the peak spurious signal amplitude, expressed in decibels (dB).

#### **Intermodulation Distortion**

With inputs consisting of sine waves at two frequencies, f<sup>A</sup> and fB, any active device with nonlinearities creates distortion products at sum and difference frequencies of m × f<sup>A</sup> and n × fB, where m, n = 0, 1, 2, 3, and so on. Intermodulation distortion terms are those for which neither m nor n are equal to 0. For example, the second-order terms include (f<sup>A</sup> + fB) and (f<sup>A</sup> − fB), and the third-order terms include (2f<sup>A</sup> + fB), (2f<sup>A</sup> − fB), (f<sup>A</sup> + 2fB), and (f<sup>A</sup> − 2fB).

The AD4086 is tested where two input frequencies near the top end of the input bandwidth are used. In this case, the second-order terms are usually distanced in frequency from the original sine waves, and the third-order terms are usually at a frequency close to the input frequencies. As a result, the second-order and third-order terms are specified separately. The calculation of the intermodulation distortion is as per the THD specification, where it is the ratio of the RMS sum of the individual distortion products to the RMS amplitude of the sum of the fundamentals, expressed in decibels.

#### **Power Supply Rejection Ratio (PSRR)**

PSRR is a measure of the sensitivity of the ADC to variations in the specified power supply rail vs. frequency. PSRR is computed as the ratio of the observed change in the output code in RMS volts to the RMS magnitude of the perturbing signal coupled to the supply. The resulting ratio is reported in decibels (dB).

**[analog.com](http://www.analog.com/en/index.html) Rev. 0 | 17 of 91**

# <span id="page-17-0"></span>**THEORY OF OPERATION**

#### **PRODUCT OVERVIEW**

The AD4086 is a high speed, low noise, low distortion, 14-bit, Easy Drive, SAR ADC. The device is capable of conversion rates up to 40MSPS, with 48.21ns result output latency. The parametric performance, bandwidth, and throughput make this product ideal for a variety of high speed, data acquisition applications. Innovations in the AD4086 product design enable both complexity reduction and component flexibility in the design of data acquisition signal chains.

The converter architecture enables continuous acquisition of the input signal throughout the entire conversion period, tCONV, reducing the input signal conditioning bandwidth required to settle to the specified resolution.

The design incorporates circuitry to reduce the nonlinear input current associated with the charge kickback typical of a switched capacitor SAR input.

Conversion result access occurs via either a multilane LVDS port operating at clock rates up to 280MHz or via a multioutput SPI operating at clock rates up to 50MHz.

The LVDS interface is compatible with differential signaling standards between 1.2V and 2.5V. To maximize throughput, the previous conversion results can be read through the entirety of the conversion period as long as the CNV+ edge and CLK+ rising edges are aligned. The LVDS interface is described in detail in the [LVDS Data](#page-41-0) [Interface Configuration](#page-41-0) section.

The single or quad lane SPI data interface is also available for CMOS level interfacing. When configured, this interface is used to access conversion results stored in the on-chip FIFO. FIFO operation is explained in the [Result FIFO](#page-52-0) section.

### **CONVERTER OPERATION**

A conventional SAR ADC typically operates in two phases—an acquisition phase, whereby the analog input voltage is acquired on the analog input pins, and followed by a conversion phase that is initiated by a conversion start signal. During the conversion phase the sampled analog input voltage is converted to a digital conversion result. In a single ADC, this is typically performed by converting the voltage from one sampling circuit. In the case of the AD4086, Figure 30 details the unique feature of this converter, whereby the analog input is connected to two sampling circuits, and the input is sampled by each one in sequence. To a user, this requires no additional control or configuration, and as such, is completely transparent in usage.

![](_page_17_Figure_12.jpeg)

*Figure 30. Simplified Representation of the AD4086 SAR ADC*

The AD4086 converter seamlessly sequences back and forth from one sampler to the other, meaning that one sampler is in acquisition mode while the voltage sampled on the other is being converted. Figure 31 shows that the AD4086 timing is contrasted against a conventional SAR ADC, where it switches between sequential conversion and the acquisition phase leads to a reduced amount of time for the input signal acquisition and settling. As sampling rates increase (and therefore cycle times reduce), it is important to maintain longer acquisition times to enable settling, particularly to the higher levels of precision offered by the AD4086. Further details on the benefits of reducing driver and noise bandwidths are described in the [Easy Drive Analog Inputs s](#page-18-0)ection.

![](_page_17_Figure_15.jpeg)

*Figure 31. Conversion Cycle Compared to Conventional SAR*

**[analog.com](http://www.analog.com/en/index.html) Rev. 0 | 18 of 91**

# <span id="page-18-0"></span>**THEORY OF OPERATION**

#### **TRANSFER FUNCTION**

The AD4086 digitizes the full-scale difference voltage of 2 × VREFIN into 2<sup>14</sup> levels, resulting in an LSB size of 366.21μV with VREFIN <sup>=</sup> 3.0V. Note that 1 LSB at 14 bits is approximately 73.1ppm.

Table 7 summarizes the mapping of input voltages to differential output codes.

![](_page_18_Figure_5.jpeg)

*Figure 32. ADC Ideal Transfer Function for the Differential Output Codes (FSR Is Full-Scale Range)*

*Table 7. Input Voltage to Output Code Mapping*

| Description      | Analog Input Voltage<br>Difference (IN+ − IN−,<br>Volts) | Digital Output Code (Twos<br>Complement, Hex) |
|------------------|----------------------------------------------------------|-----------------------------------------------|
| FS − 1 LSB       | +VREFIN × (1 − 1/213)                                    | 0x1FFF                                        |
| Midscale + 1 LSB | +VREFIN/213                                              | 0x0001                                        |
| Midscale         | 0                                                        | 0x0000                                        |
| Midscale − 1 LSB | −VREFIN/213                                              | 0x3FFF                                        |
| −FS + 1 LSB      | −VREFIN × (1 − 1/213)                                    | 0x2001                                        |
| −FS              | −VREFIN                                                  | 0x2000                                        |

#### **EASY DRIVE ANALOG INPUTS**

The AD4086 signal input consists of a fully differential input pair (IN+ and IN−), each connected to the input sampling network (series resistance (RS) and sampling capacitance (CS)) and a pair of auxiliary inputs (AUXIN+ and AUXIN−) that provide a reference to the sampling network linearization circuits. An equivalent circuit model of the analog input is presented in Figure 33.

![](_page_18_Figure_11.jpeg)

*Figure 33. Equivalent Analog Input Circuit Model*

In this model, the input sampling network was simplified to consist of two ideal switches, R<sup>S</sup> and CS, for the ADC in acquisition mode. The typical value for C<sup>S</sup> is 23.5pF and R<sup>S</sup> is 26Ω.

The parasitic capacitance related to the pin connection (CPIN) is modeled as a shunt capacitor between the pin and device ground terminal (GND). The capacitance includes parasitic capacitance formed from the physical interface, routing in the package substrate and the device input protection circuits. The CPIN value is typically 4.5pF. The input protection circuit for the AD4086 is modeled as diode clamps to the GND and VDD33 supply rails.

The external low-pass filters (LPFs) constructed from RFILTIN and CFILTIN and RFILTAUX and CFILTAUX are band-limiting filters for the primary and auxiliary paths, respectively.

The combination of RFILTIN and CFILTIN is often referred to as anti-aliasing filters because these filters do introduce a single-pole filter in the analog input signal path. However, the function of CFILTIN is more complex and must be carefully considered. Conversion through a SAR involves sampling the voltage from an internal capacitor, represented by C<sup>S</sup> in the Figure 33, which typically occurs in two phases in time, ϕ<sup>1</sup> and ϕ<sup>2</sup> . During the first phase, the ϕ<sup>1</sup> switches are closed, the ϕ<sup>2</sup> switches are opened, and the sampling capacitors (CS) are charged to the analog input voltages present at IN+ and IN−. During the second phase, the ϕ<sup>1</sup> switches are opened, the ϕ<sup>2</sup> are closed, and the ADC converts the voltage onto CS.

An additional short time phase exists where the C<sup>S</sup> charge is reset after the conversion is complete. This process repeats for each new ADC conversion. The transfer of charge from the ADC analog input pins to CS, due to the closing of the switches in each conversion cycle, creates a demand at the analog input pin. It is important to ensure that the voltage presented at the input pin is undisturbed by the internal ADC activity so that the voltage can be converted with the highest accuracy. Each new conversion presents a disturbance, or kick, at the input. The faster the ADC conversion rate is, the more frequent the occurrence of these kicks. An ADC driver is used to ensure that the input voltage, disturbed by the kick at each sampling instance, is fully settled to the required ADC resolution prior to the next sample being acquired. The ADC driver amplifier must have a wide enough output bandwidth to settle the voltage in time for each sample, which creates a signal chain

**[analog.com](http://www.analog.com/en/index.html) Rev. 0 | 19 of 91**

#### **THEORY OF OPERATION**

design constraint to ensure that there is enough time to settle to the required voltage accuracy (or ADC resolution). For this reason, a fast ADC requires a wide bandwidth driver. For high resolution ADC converters, low signal chain noise is required to obtain high resolution. A wider bandwidth can result in more noise coming through the signal chain to the ADC that can present a significant signal chain design challenge for a conventional SAR ADC. However, the AD4086 includes some unique Easy Drive features that simplify these aspects of signal chain design.

One such AD4086 feature is continuous signal acquisition. Due to its unique design, the tAQC is equal to the tCYC of the ADC, resulting in the AD4086 being in signal acquisition mode for the full duration of each ADC conversion. The input voltage has 100% of the tCYC conversion time to settle the input voltage before the next conversion, whereas a conventional ADC may need to settle in 60% of this time. More settling time results in less bandwidth required by the driver, which generally, bears a lower power requirement. In addition, because the external filters (RFILTIN and CFILTIN) must be designed with enough bandwidth for the driver to settle the input voltage, the additional settling time results in a lower cut-off. Because of this lower cut-off, more of the signal chain noise can be filtered at the inputs with these external filters.

An additional Easy Drive feature is the highly linearized analog input current. With this feature, the AD4086 presents a less challenging load to a driver amplifier and reduces any potential distortion from a driver that can occur when presented with a nonlinear input current. Figure 34 shows the typical input currents into both the differential signal pair (IN+ and IN−) and auxiliary inputs (AUXIN+ and AUXIN−).

![](_page_19_Figure_5.jpeg)

*Figure 34. Typical Input Current vs. Differential Input Voltage*

To design the external input filter, it is usual to calculate how many time constants (K) are needed for the required resolution. For n-bit converter, 1ppm can be calculated using the following formula 1ppm = 2<sup>n</sup> /1000000. To calculate the time constant from the natural log of the required setting resolution, for example, if settling to within 1ppm of 14 bits (n = 14) of the resolution required, 1ppm would represent 0.016384 LSBs (or 2<sup>n</sup> /1000000) and be calculated with the following equation:

K = ln(2<sup>n</sup> ∕ 1ppm)

K = ln(2<sup>n</sup> ∕ 0.016384 LSB) = 13.82 time constants (1)

When considering a conventional ADC, as described in the [Con](#page-17-0)[verter Operation](#page-17-0) section, where the acquisition time is only 60% of the ADC conversion cycle, there is less time available for settling. For such an ADC sampling at 40 MSPS, the driver must settle within 25ns × 0.6 or 15 ns, and settling of the input voltage within 1ppm also requires a time constant tau (τ) of 15 ns ÷ K = 1.085 ns or a bandwidth of 1/(2 × π × τ) = 147 MHz.

With the Easy Drive features of the AD4086, the result is an acquisition time of 100% of the conversion cycle that indicates only 13.86 time constants to settle within 1ppm of 14 bits resolution. However, the low analog input current of the AD4086 and the internal methods that reduce any kick back to the driver (as charge transfers from the analog input to the internal sampling capacitors at the sampling instance) reduce the required number of time constants by 9.5%. Therefore, for the 14-bit settling example, the required number of time constants (K) reduces from 13.82 to 12.51 without impact on settling or distortion.

These Easy Drive features significantly reduce the driver bandwidth required to settle. For example, at 40MSPS, settling of the input voltage within 1ppm requires a time constant tau (τ) of 25ns ÷ K = 1.998 ns, or a bandwidth of 1/(2 × π × τ) = 80 MHz. This significant reduction in the required bandwidth allows use of lower power, lower bandwidth drivers and the design of a lower bandwidth input filter to remove more driver or signal chain noise. [Table 8](#page-20-0) suggests some filter values for use with the AD4086 in some example use case conditions (with settling of the input voltage to 1LSB).

Another Easy Drive feature, as can be seen in the [Figure 33](#page-18-0), is the auxiliary signal input path. This path feeds the analog input signal to an internal linearization block, and this block feeds a correction signal to the sampled voltage. Recommended values are given in [Table 8](#page-20-0) #unique\_37/unique\_37\_Connect\_42\_table\_w3ab1b5c49\_w4ab1b5\_w5ab1. The filter on the auxiliary inputs is set for the same bandwidth as the analog input, and RFILTAUX must be set at 4 × RFILTIN. The recommended filter configuration is using a differential CFILTIN capacitor, so calculate the components as τ = RFILTIN × 2 × CFILTIN.

Note that the minimum RFILTIN must be 15Ω, and that RFILTAUX can be set from a minimum of 5Ω up to 4 × RFILTIN.

**[analog.com](http://www.analog.com/en/index.html) Rev. 0 | 20 of 91**

# <span id="page-20-0"></span>**THEORY OF OPERATION**

*Table 8. Recommended Input Filter Configurations*

| fS (MSPS) | Target Accuracy (Bit) | Required Bandwidth (MHz) | RFILTIN (Ω) | CFILTIN (pF) | RFILTAUX (Ω) | CFILTAUX (pF) |
|-----------|-----------------------|--------------------------|-------------|--------------|--------------|---------------|
| 40        | 14                    | 56                       | 25          | 56           | 100          | 14            |
| 40        | 12                    | 48                       | 25          | 66           | 100          | 16            |
| 30        | 14                    | 42                       | 25          | 75           | 100          | 18            |

# **REFERENCE BUFFER AND COMMON-MODE OUTPUT**

The AD4086 integrates a charge reservoir capacitor (CREF) and a low-drift reference buffer at the reference input pin (REFIN), eliminating the need for dedicated external components and enabling multiple AD4086 devices to share a single voltage reference.

The integrated capacitor (CREF) has a capacitance of 9.4μF ± 20%, and it is constructed from commercially available, multilayer, high dielectric (X6S), ceramic capacitors. CREF serves as the primary charge reservoir for the data converter. Integrated, in-package components, such as CREF, minimize the overall solution area, mitigate potential performance errors introduced by factors like component selection, reduce placement and routing challenges, and in general, reduce the engineering effort to the first design success.

Additional external capacitance (CRSV) can be placed across the REFIN and REFGND pins for improved charge capacity and noise rejection as required. As with all precision circuits, the placement of the external reference capacitors must be as close to the device pins as possible on the same side of the PCB. The routing between the capacitor and device pins must minimize the series impedance in each routing path.

![](_page_20_Figure_8.jpeg)

*Figure 35. REFIN and CMO Internal Equivalent Circuit and Typical Application*

The AD4086 internally generates a common-mode reference voltage of one-half of VREFIN that is output through the CMO pin. The absolute error in the CMO output voltage is guaranteed to be less than ±20mV. The CMO output is used to set the common-mode output voltage of the analog front-end stage driving the AD4086 inputs, ensuring the AD4086 common-mode input requirement is satisfied. The CMO output must be filtered with an RC LPF to limit the total output noise as illustrated in Figure 35 (see RCMF and CCMF).

The output is generated using a resistive divider connected to the reference buffer output. The resulting output impedance at the CMO pin is typically 700Ω. Due to the limited drive capability at the CMO pin, the external load must be carefully considered to avoid excessive start-up times or absolute errors. The CMO output may be directly connected to a high impedance common-mode input of a fully differential amplifier driving the AD4086, assuming the charging time for the preceding noise limiting filter does not impact the start-up time required for the application. In general, consider CMO buffering for the following situations:

- ► The VDD33 power rail of the AD4086 is frequently cycled.
- ► Short start-up settling times are required.
- ► If the external load on CMO exceeds 30μA (R<sup>L</sup> < 45kΩ). See [Figure 24](#page-14-0) for the typical load regulation information.

# **POWER SUPPLIES**

The power requirements for the AD4086 are distributed across a minimum of three supply domains including a 3.3V analog circuit domain (VDD33), a 1.1V core supply (VDD11), and a 1.1V domain for the digital interface (IOVDD). An optional fourth supply rail (VDDLDO) can be used to supply power to two integrated voltage regulator used to internally power the 1.1V core (VDD11) and interface (IOVDD) rails. Each of these two regulators can be independently turned off by software. For all details and design considerations when using the internal voltage regulators, see the [Internally Regulated Supply Configuration](#page-21-0) section. On the other hand, for applications that will not use internal regulators see the [Externally Generated Supply Configuration](#page-21-0) section for further details.

Power for the VDD33 supply rail must be supplied from an external source and must only be applied once power is supplied to the 1.1V supply rails as described in the [Power Supply Sequence](#page-22-0) section.

**[analog.com](http://www.analog.com/en/index.html) Rev. 0 | 21 of 91**

# <span id="page-21-0"></span>**THEORY OF OPERATION**

![](_page_21_Figure_2.jpeg)

*Figure 36. Typical Regulator Start-Up Transient, Converter Idle*

All supply domains are internally decoupled using multilayer, high dielectric, ceramic capacitors (X6S), eliminating the need of external decoupling capacitors. However, care must be taken to understand the bulk decoupling requirements for other components in the design that share the same supply. Integrated supply decoupling capacitors in the AD4086 are listed in [Table 6](#page-8-0) as well as in Table 9.

*Table 9. Integrated Supply Decoupling Summary*

| Supply Pin | Nominal Value (μF) | Tolerance (%) | Return Path |
|------------|--------------------|---------------|-------------|
| VDD33      | 0.47               | ±10           | GND         |
| VDDLDO     | 0.22               | ±10           | GND         |
| VDD11      | 1.88 (4× 0.47)     | ±10           | GND         |
| IOVDD      | 0.22               | ±10           | IOGND       |

### **INTERNALLY REGULATED SUPPLY CONFIGURATION**

The AD4086 includes two internal LDO regulators, one to generate the 1.1V VDD11 supply rail and another to internally generate the 1.1V IOVDD supply rail. Upon power on or reset of the AD4086 registers, both regulators automatically power up when an external voltage source in the range of 1.4V to 2.7V is applied to the VDDLDO pin. The regulators are designed to supply the internal load requirement of the AD4086; therefore, no external loading is permitted. Note that, as described in the [Power Saving Operating](#page-23-0) [Modes](#page-23-0) section, IOVDD is disabled in both power saving modes.

The required connectivity when using the internal regulators is illustrated in Figure 37. As shown in Figure 37, the VDD11 pins (A1, A2, and A3) must be shorted together. It is recommended that a thick trace or polygon on the device side of the PCB be used to implement this connection in the physical design to minimize routing impedance. The VDD33 rail is supplied with an external 3.3V supply. This supply can be removed when using power saving modes. When this supply is removed, only analog circuity is held in reset, and the configuration register content remains unaffected. Refer to [Table 1](#page-2-0) for the applicable input voltage tolerance for each supply rail.

![](_page_21_Picture_10.jpeg)

*Figure 37. Internally Regulated (1.1V) Supply Configuration*

The internally regulated configuration is ideal for use in area constrained applications where the ability to eliminate external regulators is advantageous. However, note that, in this configuration, the internal supply regulation introduces additional power dissipation.

# **EXTERNALLY GENERATED SUPPLY CONFIGURATION**

In system using externally generated supplies VDDLDO must be left unconnected. With VDDLDO unconnected both the internal LDO powering VDD11 and the internal LDO powering IOVDDD are automatically disabled. VDD11 must be connected to an externally generated 1.1V supply rail, and IOVDD should be connected to an externally generated 1.1V to 1.2V supply rail. It should be noted that if VDD11 is not present, the device will be held in a power-on reset (POR) state, and all AD4086 registers reset to their default state after the supply has been reestablished. More details on the POR circuitry can be found in the Power-On Reset (POR) Monitor section. The VDD33 rail is supplied with an external 3.3V supply. The VDD33 supply can be removed to further reduce power (see the [Power Saving Operating Modes](#page-23-0) section), only analog circuity is held in reset, and the register content remains unaffected. Refer to [Table 1](#page-2-0) for the applicable input voltage tolerance for each supply rail.

As illustrated in the example of Figure 38, external voltage sources are applied to VDD11 and IOVDD pins.

![](_page_21_Figure_16.jpeg)

*Figure 38. Externally Sourced Supply Configuration*

#### **POWER-ON RESET (POR) MONITOR**

The AD4086 power supply monitoring circuits inhibit the converter functions and reset the configuration memory when supply conditions are outside the specified operating limits. This function ensures each device is in a deterministic state after power-up. The power-on function is constructed from two independent voltage monitors, the first measuring the core 1.1V supply and a second

**[analog.com](http://www.analog.com/en/index.html) Rev. 0 | 22 of 91**

# <span id="page-22-0"></span>**THEORY OF OPERATION**

measuring the voltage at the reference input pin (REFIN). Each monitor has its own comparator output that is used to decouple the analog and digital block resets as shown in Figure 39.

![](_page_22_Figure_3.jpeg)

*Figure 39. Simplified Diagram of POR Circuit*

The core VDD (1.1V) supply monitor compares the VDD11 supply voltage against a preset threshold of 0.93V. If the supply voltage falls to less than this threshold, a reset signal, POR\_D, asserts. The digital logic reset signal, DIG\_RESET, is defined as the logical combination of the POR\_D signal and (logical AND) the compliment of the SPI software reset function. When either the POR\_D signal (VDD11 < 0.93V) or the SW RESET signal is asserted, the internal digital circuitry is held in reset. When cleared, the contents of the configuration registers are restored to the factory default settings.

The reference monitor compares the input voltage at REFIN against a preset threshold of 2.7V. As illustrated in Figure 39, power for the reference monitor circuit is supplied from the VDD33 supply. However, it is important to note that a reference voltage below 2.6V will cause the device to stop outputting conversion data results. To recover the conversion process, the reference voltage needs to be brought to 2.87V. For correct operation of the monitor circuit, the VDD33 supply must be applied to the AD4086 within the specified tolerance of 3.3V ± 5% before the reference source is enabled. Assuming the device is operating within the specified supply conditions, a reference voltage less than 2.7V results in the assertion of an internal reset signal, POR\_A. The POR\_A signal and (logical AND) the DIG\_RESET signal are combined to produce a reset (ANA\_RESET) for the analog circuit blocks including the ADC core, ADC timer, reference buffer, and so forth. If this reset signal is asserted, the analog blocks are placed in an inactive state, and the converter functionality is disabled. This event is indicated with a value of 1 in the POR\_ANA\_FLAG bit from the [Device](#page-78-0) [Status Register](#page-78-0) (Address 0x14). The state of the event detection is persistent until a Logic 1 is written to the POR\_ANA\_FLAG bit to clear the detection state.

#### **POWER SUPPLY SEQUENCE**

Table 10 specifies the recommended supply sequences for both internal and external generation of 1.1V supply rails (IOVDD and VDD11). Both methods are shown in [Figure 40](#page-23-0) and [Figure 41,](#page-23-0) where the supplies that must be provided to the AD4086 are highlighted in blue, including the REFIN voltage. In both cases, the AD4086 requires that the supplies are applied in ascending voltage order. The design must also ensure that voltage is applied at the analog inputs (IN+ and IN−) and reference input (REFIN) concurrently with, or immediately following, the VDD33 supply. Failing in providing REFIN reference voltage on power up will result in no ADC conversions at the output of the ADC, and it will continue to do so until REFIN voltage is provided. Note that test pattern described in the [Data Interface Test Functions](#page-47-0) section will not work in the previously mentioned case when a voltage reference is not provided at the power up. However, if reference voltage was provided at power up and then removed, the test pattern will still work and output the correct data. As described in the [Power-On Reset \(POR\) Monitor](#page-21-0) section, the voltage at the reference input pin must only be applied once VDD33 is within the specified supply tolerance to avoid undesired behavior. Therefore, if the selected voltage reference does not provide an enable pin, it is strongly recommended to design the reference circuit to power up after VDD33. After reset or POR, there are 300μs required before the device can be accessed; this is to assure the device has completed the initialization procedures. If this condition is not met, NOT\_READY\_ERR bit will be asserted of the INTERFACE\_STATUS\_A (0x11).

The configuration SPI inputs, CS, SCLK, and SDI, are protected with clamps to the VDD33 supply rail to allow the inputs to swing more than IOVDD. As a consequence of this architectural decision, it is necessary to either drive the SPI inputs to ground or to otherwise leave the inputs floating until VDD33 is greater than IOVDD − 0.3V. Alternatively, the VDD33 source can be connected to the device using a series power switch, like the [ADP199,](https://www.analog.com/adp199) configured so that the switch is open when the source is less than IOVDD − 0.3V, eliminating the parasitic current path through the digital inputs to VDD33.

*Table 10. Recommended Supply Sequence*

| 1.1V Supplies (IOVDD and VDD11) Source | Supply Sequence              |
|----------------------------------------|------------------------------|
| Internally Generated                   | 1.<br>VDDLDO                 |
|                                        | 2.<br>VDD33                  |
|                                        | 3.<br>Digital inputs         |
|                                        | 4.<br>Input drive, reference |
| Externally Generated                   | 1.<br>IOVDD, VDD11           |
|                                        | 2.<br>VDD33                  |
|                                        | 3.<br>Digital inputs         |
|                                        | 4.<br>Input drive, reference |

To power down the application circuit, the power-up sequence specified in Table 10 should be reversed.

**[analog.com](http://www.analog.com/en/index.html) Rev. 0 | 23 of 91**

# <span id="page-23-0"></span>**THEORY OF OPERATION**

![](_page_23_Figure_2.jpeg)

*Figure 40. Power Supply Sequence, Internally Generated IOVDD, VDD11*

![](_page_23_Figure_4.jpeg)

*Figure 41. Power Supply Sequence, Externally Generated IOVDD, VDD11*

### **POWER SAVING OPERATING MODES**

The operating mode of the AD4086 is controlled by the OPERAT-ING\_MODES bits in the device configuration register (see the [De](#page-71-0)[vice Configuration Register](#page-71-0) section, Address (0x02)). On power-up and after reset, the default is normal mode (OPERATING\_MODES = 00). [Table 11](#page-24-0) describes all operating modes, and Figure 42 depicts the allowed transitions between these modes. Note that direct transitions between the two power saving modes (standby mode and sleep mode) are not permitted.

It is important to stop all conversion and data interface clocking before configuring the power mode.

When in either standby mode or sleep mode, the VDD33 supply can be removed to reduce power consumption. This supply must be re-established prior to issuing the SPI configuration interface command to exit either power saving mode.

![](_page_23_Picture_11.jpeg)

*Figure 42. Operating Mode Transitions*

Transitioning from normal mode to either of the two power saving modes is achieved by writing the required value to the OPERAT-ING\_MODES bits in the device configuration register (see the [Device Configuration Register](#page-71-0) section). Waking up (that is, transi-

**[analog.com](http://www.analog.com/en/index.html) Rev. 0 | 24 of 91**

# <span id="page-24-0"></span>**THEORY OF OPERATION**

tioning back to normal mode) is achieved in a similar way, because the SPI configuration interface operation is not affected by any of the power saving modes (see the [SPI Configuration Interface](#page-31-0) section). Standby mode can be selected to save power in the case where the user wants to quickly return to normal conversions. Sleep mode is a lower power state where returning to normal mode takes longer. Both standby and sleep mode can be particularly useful when used with the result FIFO (see the [Result FIFO](#page-52-0) section), whereby previously stored conversion data can be accessed from the FIFO while it is still in the selected power saving mode.

To reduce power consumption in both standby and sleep modes, the internal IOVDD LDO regulator is powered down. If the user is not externally supplying IOVDD, all IOVDD domain inputs and outputs are disabled (all GPIOx, all LVDS data interface (see the [LVDS Data Interface](#page-41-0) section), and SPI data interface (see the [SPI Data Interface](#page-47-0) section) signals are disabled. In this specific condition, it is still possible to write to the AD4086 SPI configuration to issue a command to return to normal mode by writing to the OPERATING\_MODES bits in the device configuration register (see the [Device Configuration Register](#page-71-0) section) or to issue a software reset (see the [Software Reset](#page-25-0) section). As GPIOx is disabled, it is not possible to perform any read activity on the SPI configuration interface bus.

When IOVDD is externally supplied, and the device is put into standby or sleep mode, the LVDS data interface is disabled; however, all GPIOx, SPI data interface, and SPI configuration interface pins remain enabled and unaffected. While power is supplied externally to IOVDD within its specified range, previously acquired data stored in the result FIFO can be access in either standby or sleep mode.

Table 11 also indicates the wake-up times associated with each of the modes. Wake-up time from sleep mode is significantly higher than that of standby mode, because time must be allowed for the internal reference and common-mode buffers to re-enable and to replenish charge to the internal capacitors. When returning to normal mode, the specified wake-up time must be satisfied before applying the first conversion start pulse. This specified time is the time it takes from when the SPI command to exit the selected power saving mode is written to the device configuration register (see the [Device Configuration Register](#page-71-0) section) to update the OPERATING\_MODES bits.

For the lowest power consumption in any of the power saving operating modes, the LVDS\_SELF\_CLK\_MODE must be enabled in the ADC Data Interface Configuration B register (see the [ADC](#page-80-0) [Data Interface Configuration B Register](#page-80-0) section) to power down the LVDS DCO transmitter.

*Table 11. Power Saving Operating Modes*

| Operating<br>Mode | OPERATING_MODES<br>Bits Value | Description              | Effect                                                                                                                                                                                                                                                                                                                                                                                                                                    | Wake-Up Time (Maximum Time to<br>Normal Mode) |
|-------------------|-------------------------------|--------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------|
| Normal            | 0b00                          | Normal operating mode    | Normal operation.                                                                                                                                                                                                                                                                                                                                                                                                                         | Not applicable                                |
| Standby           | 0b10                          | Standby operating mode   | The internal IOVDD LDO regulator is disabled.<br>If IOVDD is not externally supplied, all GPIOx and all<br>LVDS data interface and SPI data interface signals<br>are disabled. For the SPI configuration interface only,<br>writes to the device configuration register (see the<br>Device Configuration Register section) and Interface<br>Configuration A register (see the Interface Configuration<br>A Register section) are allowed. | 100μs                                         |
|                   |                               |                          | If IOVDD is externally supplied, all GPIOx and SPI data<br>interface signals are enabled. The SPI configuration<br>interface is fully enabled. Because the SPI data<br>interface remains enabled, the user can access data<br>in the result FIFO (see the Result FIFO section).                                                                                                                                                           |                                               |
|                   |                               |                          | The ADC core is powered down. The analog circuitry<br>remains in reset (ANA_RESET remains asserted), and<br>no ADC conversions can be performed.                                                                                                                                                                                                                                                                                          |                                               |
|                   |                               |                          | The VDD33 supply can be removed to reduce power.<br>When in use, the internal VDD11 LDO regulator remains<br>on.                                                                                                                                                                                                                                                                                                                          |                                               |
|                   |                               |                          | The internal reference buffer is enabled.                                                                                                                                                                                                                                                                                                                                                                                                 |                                               |
|                   |                               |                          | The common-mode output buffer is enabled.                                                                                                                                                                                                                                                                                                                                                                                                 |                                               |
|                   |                               |                          | The LVDS interface is disabled.                                                                                                                                                                                                                                                                                                                                                                                                           |                                               |
| Sleep             | 0b11                          | Low power operating mode | The internal IOVDD LDO regulator is disabled.                                                                                                                                                                                                                                                                                                                                                                                             | 180μs                                         |
|                   |                               |                          | If IOVDD is not externally supplied, all GPIOx and all<br>LVDS and SPI data interface signals are disabled. For<br>the SPI configuration interface only, writes to the device                                                                                                                                                                                                                                                             |                                               |

**[analog.com](http://www.analog.com/en/index.html) Rev. 0 | 25 of 91**

# <span id="page-25-0"></span>**THEORY OF OPERATION**

*Table 11. Power Saving Operating Modes (Continued)*

| Operating<br>Mode | OPERATING_MODES<br>Bits Value | Description | Effect                                                                                                                                                                                                                                                                          | Wake-Up Time (Maximum Time to<br>Normal Mode) |
|-------------------|-------------------------------|-------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------|
|                   |                               |             | configuration register (see the Device Configuration<br>Register section) and Interface Configuration A register<br>(see the Interface Configuration A Register section) are<br>allowed.                                                                                        |                                               |
|                   |                               |             | If IOVDD is externally supplied, all GPIOx and SPI data<br>interface signals are enabled. The SPI configuration<br>interface is fully enabled. Because the SPI data<br>interface remains enabled, the user can access data<br>in the result FIFO (see the Result FIFO section). |                                               |
|                   |                               |             | The ADC core is powered down. The analog circuitry<br>remains in reset (ANA_RESET remains asserted), and<br>no ADC conversions can be performed.                                                                                                                                |                                               |
|                   |                               |             | The VDD33 supply can be removed to reduce power.                                                                                                                                                                                                                                |                                               |
|                   |                               |             | The internal reference buffer is disabled.                                                                                                                                                                                                                                      |                                               |
|                   |                               |             | When enabled, the internal VDD11 LDO regulator<br>remains on.                                                                                                                                                                                                                   |                                               |
|                   |                               |             | The common-mode output buffer is disabled.                                                                                                                                                                                                                                      |                                               |
|                   |                               |             | The LVDS interface is disabled.                                                                                                                                                                                                                                                 |                                               |
|                   |                               |             | The SPI data interface remains enabled to access data<br>in the result FIFO (see the Result FIFO section).                                                                                                                                                                      |                                               |

To avoid device damage additional recovery time has to be added when coming out of the standby or sleep mode. This time is required from the time when part is back to normal mode and is counted until the next conversion clock as indicated on the plot Figure 43.

![](_page_25_Figure_5.jpeg)

*Figure 43. Recovery Time After Standby/Sleep Mode*

#### **SOFTWARE RESET**

This reset method must only be used once the AD4086 is in an idle state, where conversions are not being clocked, and any existing conversion is completed.

A software reset is achieved by issuing the following two writes to the Interface Configuration A register (see the [Interface Configura](#page-70-0)[tion A Register](#page-70-0) section, Address 0x00):

- **1.** Set SW\_RESET and SW\_RESETX bits to 1 by writing 0x81 to the register.
- **2.** Then, issue another write command that sets either or both of those bits to 0 to initiate the reset.
- **3.** Software reset initialization will require 300μs. During this initialization time, reading the NOT\_READY\_ERR in the INTER-FACE\_STATUS\_A register will return a 1 until the initialization is complete. Once the software reset initialization is complete, the part is now reset and NOT\_READY\_ERR will return to 0. SPI configuration writes will be ignored while during this initialization when NOT\_READY\_ERR is set to 1.

This action returns any previously configured registers to their default settings, except for the ADDR\_ASCENSION bit from the Interface Configuration A register, which keeps its previous value. The contents of the FIFO, if any, are also not affected by the software reset. The ADDR\_ASCENSION bit and FIFO data only return to their default settings after a hardware reset or a full power-up happens. The NOT\_READY\_ERR flag of the INTERFACE\_STATUS\_A register (0x11) will assert if a 300μs minimum time after setting software reset bits (SW\_RESET & SW\_RESETX) is breached.

**[analog.com](http://www.analog.com/en/index.html) Rev. 0 | 26 of 91**

# <span id="page-26-0"></span>**APPLICATIONS INFORMATION**

#### **TYPICAL APPLICATIONS DIAGRAMS**

![](_page_26_Figure_3.jpeg)

*Figure 44. AD4086 Typical Applications Diagram, Fully Differential Amplifier*

![](_page_26_Figure_5.jpeg)

*Figure 45. AD4086 Typical Applications Diagram, Single Op-Amp Drivers*

**[analog.com](http://www.analog.com/en/index.html) Rev. 0 | 27 of 91**

# <span id="page-27-0"></span>**APPLICATIONS INFORMATION**

#### **ANALOG FRONT END DESIGN**

### **Driver Amplifier Choice**

As described in the [Easy Drive Analog Inputs](#page-18-0) section, the AD4086 has a number of unique features that open this ADC up to being used with a wide range of driver amplifier solutions. Because the AD4086 offers exceptionally low noise and excellent levels of precision at sampling rates up to 40MSPS with remarkably efficient power consumption, signal chain choices on which application parameters to prioritize is presented. As is often the case, there can be some competing parameters to consider. Wider bandwidth amplifiers are required to drive faster ADCs because the settling

bandwidth, signal bandwidth, and the noise bandwidth increase. In addition, as these speeds increase, maintaining precision in a driving amplifier becomes a greater challenge. These challenges are often met by increased power in the driver; however, Analog Devices, Inc., offers a wide choice of power efficient driver amplifiers that can be found on the [Differential Amplifiers and ADC Drivers](https://www.analog.com/en/product-category/differential-amplifiers-and-adc-drivers.html) web page. Also, due to the Easy Drive features of the AD4086, where the settling bandwidth is relaxed considerably, products such as the [ADA4945-1 f](https://www.analog.com/ada4945-1)ully differential amplifier (FDA) make an excellent low power companion product. Table 12 offers some other suggested products for consideration.

*Table 12. Driver Amplifier Selection Table*

| Part Number | Category      | Quiescent<br>Current (IQ) | Input Voltage<br>Noise (VN) | −3dB Bandwidth<br>(Gain = 1) | THD at 1MHz | Application Considerations                                                      |
|-------------|---------------|---------------------------|-----------------------------|------------------------------|-------------|---------------------------------------------------------------------------------|
| ADA4945-1   | FDA           | 4mA                       | 1.8nV/√Hz                   | 145MHz                       | −90dB       | Lowest power                                                                    |
| ADA4932-1   | FDA           | 9.6mA                     | 3.6nV/√Hz                   | 560MHz                       | −110dB      | Low power, wider bandwidth, improved distortion<br>at higher signal frequencies |
| ADA4927-1   | FDA           | 20mA                      | 1.3nV/√Hz                   | 2300MHz                      | −112dB      | Low noise, lower distortion at higher signal fre<br>quencies                    |
| AD8139      | FDA           | 24.5mA1                   | 2.25nV/√Hz                  | 410MHz                       | −120dB      | Lowest distortion at higher signal frequencies                                  |
| ADA4899-1   | Single op amp | 28.6mA1                   | 1.414nV/√Hz                 | 600MHz                       | −117dB      | Lowest distortion at higher signal frequencies                                  |
| ADA4930-1   | FDA           | 35mA                      | 1.15nV/√Hz                  | 1350MHz                      | −110dB      | Lowest noise                                                                    |

<sup>1</sup> Combined quiescent current of two amplifiers.

**[analog.com](http://www.analog.com/en/index.html) Rev. 0 | 28 of 91**

# <span id="page-28-0"></span>**APPLICATIONS INFORMATION**

#### **REFERENCE CIRCUITRY DESIGN**

The AD4086 requires a low noise, high precision and stability, and low temperature drift external reference of 3V. This reference defines a differential input range for the ADC of ±VREFIN. The reference must be within ±5mV of +3V. Recommended references are [LTC6655](https://www.analog.com/ltc6655), [LT6657](https://www.analog.com/lt6657), or [ADR4530](https://www.analog.com/adr4530). For best performance, however, use the LTC6655 external reference. Table 13 details the typical parameters of the previously mentioned references, comparing absolute accuracy, noise, temperature drift, load regulation, and power consumption. For more detailed specifications, refer to the data sheet of the given product.

*Table 13. Comparison of the Main Parameters of the LTC6655, LT6657, and ADR4530 References*

| Parameter                           | LTC6655 | LT6657 | ADR4530B |
|-------------------------------------|---------|--------|----------|
| Accuracy                            | 0.025%  | 0.1%   | 0.02%    |
| Temperature Coefficient<br>(ppm/°C) | 2       | 1.5    | 2        |
| 0.1Hz to 10Hz Noise (ppm p-p)       | 0.25    | 0.5    | 0.53     |
| Maximum Load (mA)                   | ±5      | ±10    | ±10      |
| Load Regulation (ppm/mA)            | 3       | 0.7    | 30       |
| Maximum Supply (V)                  | 13.2    | 40     | 15       |
| Shutdown                            | Yes     | Yes    | No       |
| Supply Current, IS (mA)             | 5       | 1.2    | 0.7      |

There is no need for the external reference capacitor because the AD4086 embeds one internally, 9.4μF, (see Figure 46). The REFIN reference input pin is internally buffered, which substantially reduces ADC conversion transients and isolates the external reference from these transients. Therefore, no external amplifier is required to buffer the external reference. For the reference input capacitance (C REF IN) and reference output capacitance (C REF OUT) values, refer to the given external reference IC data sheet recommendations. As a layout recommendation, the external reference chip must be placed as close as possible to the AD4086 and its REFIN pin to minimize the series impedance of the track connecting the REFIN pin to the external reference output. It is recommended to minimize the exposure of this track to noisy signals, especially digital ones.

![](_page_28_Figure_7.jpeg)

*Figure 46. AD4086 General External Reference Design Functional Diagram*

### **DATA INTERFACE CLOCKING SOLUTION**

When designing the LVDS data interface (see the [LVDS Data Inter](#page-41-0)[face](#page-41-0) section), the user must ensure the clocking solution adheres to the timing specifications of the AD4086 (see [Table 2](#page-5-0)). When configured for LVDS mode data interface, the user must ensure that timing specifications stay within the maximum conversion to clock alignment time of ±535ps (tCCA). In addition, ensure that a low jitter conversion (CNV) clock is provided such that there is no unwanted impact to SNR performance. This jitter is signal frequency dependent; therefore, the level of jitter tolerable in a given system is dependent on the application use case. The Analog Devices technical article [Maximum SNR vs Clock Jitter](https://www.analog.com/en/resources/technical-articles/maximum-snr-vs-clock-jitter.html) provides further guidance on this topic.

For example, a recommended clocking solution for where the AD4086 is configured to use the LVDS data interface with a single lane enabled and using echo clock mode. In this example, a 25MHz oscillator is selected with low phase noise and jitter. The [MT-008](https://www.analog.com/MT-008) tutorial serves as an aid to convert between phase noise and RMS phase jitter, often quoted interchangeably in crystal oscillator product data sheets. The [ADF4350](https://www.analog.com/adf4350) wideband synthesizer with an integrated voltage-controlled oscillator (VCO) serves as versatile means of generating a 280MHz clock system clock, while maintaining low jitter and offering flexibility and control to reconfigure this frequency depending on the application needs. This clock then feeds the [AD9508](https://www.analog.com/ad9508) clock fanout buffer with output dividers that can be configured for the desired LVDS level signaling. In the example shown in [Figure 47,](#page-29-0) one output channel is set to divide by 1 to output the LVDS clock, while another output channel is configured to divide by 7 to output the AD4086 conversion clock. This 1:7 ratio of CNV:CLK frequencies ensures 14 bits of data can be read out in on the double data rate (DDR), single lane, LVDS data interface. For a dual lane configuration, such as shown in [Figure 48,](#page-29-0) this ratio is adjust to 1:4.

The example shows that echo clock mode is used and aids data alignment for the host controller (in the case a field-programmable gate array (FPGA)). In self clock mode, where DCO+ and DCO−

**[analog.com](http://www.analog.com/en/index.html) Rev. 0 | 29 of 91**

# <span id="page-29-0"></span>**APPLICATIONS INFORMATION**

are not available for alignment, the [ADC Result Latency and LVDS](#page-44-0) [Interface Alignment](#page-44-0) section describes how the INTF\_CHK\_EN bit (Address 0x15, Bit 4) can be enabled to help align the host controller to data and to mitigate against any system propagation delays.

![](_page_29_Figure_3.jpeg)

*Figure 47. Single Lane, LVDS Data Interface Clocking Example*

![](_page_29_Figure_5.jpeg)

*Figure 48. Dual Lane, LVDS Data Interface Clocking Example*

In cases where the SPI data interface (see the [SPI Data Interface](#page-47-0) section) is used to access conversion results from the result FIFO (see the [Result FIFO](#page-52-0) section) again, it is important that the CNV source jitter is carefully considered to achieve the required performance. In the case shown in the SPI data interface clocking example (see Figure 49), an oscillator directly provides the conversion clock, and the data is asynchronously clocked from the FIFO by a microcontroller unit (MCU). Optionally, as shown in Figure 49, the general-purpose input and output pins can be configured to control the result FIFO operation (see the [GPIO Pins](#page-48-0) section and the [Result FIFO](#page-52-0) section).

![](_page_29_Figure_8.jpeg)

*Figure 49. SPI Data Interface Clocking Example*

#### **POWER SOLUTION**

With such low noise and up to a 40MHz sampling rate, it is important that careful consideration is taken for the power solution of applications to ensure that the low noise supplies provided to the AD4086 do not become a source of performance or accuracy degradation. To aid ease of use and to help reduce external required components, two internal LDO regulators are integrated within the AD4086. Further details on these regulators can be found in the [Internally Regulated Supply Configuration](#page-21-0) section. Also, note that the internal supply decoupling capacitors are included for all supply rails, whether generated internally or externally, reducing external component count, simplifying use, and offering huge benefits to PCB layout, routing, and design density.

For externally generated supply rails, excellent choice LDO regulators are the [LT3045 o](https://www.analog.com/lt3045)r [ADP150](https://www.analog.com/adp150), which both offer ultra-low noise and excellent power supply rejection. For high efficiency, step-down switching regulators, the [LT8604C](https://www.analog.com/lt8604) is a good choice; however, great care must be taken in the design of the switching regulator circuity because switching frequencies are likely to be within the application signal bandwidth, and although the AD4086 has high AC power supply rejection on its supplies, appropriate consideration must be given to the supply rails.

**[analog.com](http://www.analog.com/en/index.html) Rev. 0 | 30 of 91**

#### <span id="page-30-0"></span>**DIGITAL INTERFACE**

# **OVERVIEW**

The AD4086 digital interface consists of a 4-wire SPI for device configuration, four general-purpose input and output (GPIO) pins, a conversion data access interface with selectable output format (LVDS or SPI data interface), and a conversion start input (CNV+ and CNV−) that can be configured for LVDS or CMOS level signaling.

# **ADC CONVERSION CONTROL**

The ADC acquires a sample and initiates a conversion operation on the rising edge of the convert start signal, applied at the CNV+ and CNV− pins. There are two possible configurations for the electrical signaling at the convert start input pins: CMOS or LVDS.

CMOS is the default mode on power-up and after reset. CMOS requires that the CNV− pin be tied to the digital interface ground (IOGND). In this mode, the convert signal must be a CMOS logic signal referenced to IOGND and applied at CNV+, with logic levels according to the parameters of the digital inputs (CNV, GPIOx, DCS, and DCLK) in [Table 1](#page-2-0).

To switch to LVDS mode, the LVDS\_CNV\_EN bit of the ADC Data Interface Configuration B register (see the [ADC Data Interface Con](#page-80-0)[figuration B Register s](#page-80-0)ection, Address 0x16) must be set to 1. In this mode, an external 100Ω termination resistor must be installed between the CNV+ and CNV− pins, as close to the AD4086 as possible. In LVDS mode, the CNV+ and CNV− pins must be driven differentially with an LVDS driver conforming to the levels specified

in the LVDS I/O (EIA-644) parameters in [Table 1](#page-2-0). Care must be taken to closely match the CNV+ and CNV− differential signal pair routing and to use controlled impedance to ensure signal integrity.

#### **SPI REGISTER INTERFACE**

The configuration register interface is an SPI that enables both device configuration and system status monitoring. This interface is configured for 4-wire, full-duplex operation. Dedicated interface pins for the interface chip select (CS), serial clock (SCLK), and serial data input (SDI) are intended for direct connection to the host controller. By default, at power-up or after a software reset, the configuration interface SDO function is enabled and assigned to the GPIO0 pin.

The configuration interface timing convention implemented in this design is consistent with SPI Mode 3, clock polarity (CPOL) = 1, clock phrase (CPHA) = 1. As such, the serial clock (SCLK) is expected to idle high, and the state of the data pins, SDI and SDO, are updated on the falling (leading) edge of the clock, such that these pins can be sampled on the subsequent rising (trailing) edge. See the Analog Dialogue article, [Introduction to SPI Interface,](https://www.analog.com/en/resources/analog-dialogue/articles/introduction-to-spi-interface.html) for more details regarding the SPI and SPI modes.

The memory access controller associated with this interface supports a number of user-programmable options accessible through the interface configuration memory space (Address 0x00 to Address 0x11). The available options for the AD4086 are listed and described in Table 14.

| Interface Option                                   | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
|----------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Software Reset (SW_RESET,<br>SW_RESETX)            | Resets the internal configuration memory to the default state (except for ADDR_ASCENSION bit). Data FIFO is unaffected. Only use this<br>reset method once the ADC is in an idle state, where conversions are not clocked, and any existing conversion is completed. See the<br>Software Reset section for details.                                                                                                                                                                                                              |
| Address Ascension<br>(ADDR_ASCENSION)              | Selecting this option changes the behavior of the memory controller address counter from decrementing (default) to incrementing. This<br>change affects multibyte transfers, for example, when accessing a multibyte register as a single entity or when streaming mode is enabled.<br>The selection impacts the starting address for multibyte register accesses in strict register access mode. See the Address Ascension<br>Selection section for details.                                                                    |
| Short Instruction<br>(SHORT_INSTRUCTION)           | Selecting this option reduces the length of the address field in the instruction word from 15 bits to 7 bits.                                                                                                                                                                                                                                                                                                                                                                                                                    |
| Single Instruction<br>(SINGLE_INST)                | Selecting this option changes from the default streaming mode to single instruction mode, which requires the host controller to transmit an<br>instruction for each register access within a given SPI frame. The size of an entity is dependent on the strict register access setting and<br>whether or not the register is multibyte. This feature allows random access to the memory space during configuration. See the Instruction<br>Mode Selection section for details.                                                   |
| Strict Register Access<br>(STRICT_REGISTER_ACCESS) | Selecting this option instructs the memory controller to treat a multibyte register as a single entity, generating a fault when a partial access<br>is attempted. See the Strict Access Selection and Multibyte Registers section for details.                                                                                                                                                                                                                                                                                   |
| CRC Enable (CRC_ENABLE,<br>CRC_ENABLEB)            | Selecting this option enables a cyclic redundancy check (CRC) to verify the integrity of data sent to and received from the host. See the<br>Configuration Cyclical Redundancy Check (CRC) section for details.                                                                                                                                                                                                                                                                                                                  |
| Status Data Transmission<br>(SEND_STATUS)          | Selecting this options enables the transmission of status data through the SDO line during the instruction phase of the data frame. See<br>theStatus Data Transmission section for details.                                                                                                                                                                                                                                                                                                                                      |
| Loop Count (LOOP_COUNT)                            | Sets the data byte count before looping to the start address. When streaming data, a nonzero value sets the number of data bytes written<br>before the address loops back to the start address. A maximum of 255 bytes can be written using this approach. A value of 0x00 disables<br>the loop back so that addressing wraps around at the upper and lower limits of the memory. After writing this register, the loop value applies<br>only to the following SPI instruction and auto clears upon the end of that instruction. |

**[analog.com](http://www.analog.com/en/index.html) Rev. 0 | 31 of 91**

# <span id="page-31-0"></span>**DIGITAL INTERFACE**

# **ADC CONVERSION DATA INTERFACE**

Two signaling format options are available to access conversion results:

- ► LVDS level signaling (LVDS data interface)
- ► CMOS level signaling (SPI data interface)

The choice of interface is usually determined by the requirements and constraints of the application at hand. For example, if continuous fast data acquisition is required, then the LVDS signaling interface is typically the preferred option. If the application requires only noncontinuous bursts of data acquisitions, then either the LVDS or the SPI data interfaces can be used. The capabilities of the digital interface host can also determine which interface option is chosen.

Common to both the LVDS and SPI data interfaces are the following flexible features that reduce the burden on the chosen digital host:

- ► Multilane data transfer: enables sustained data throughput at reduced interface clock speeds.
- ► Test pattern generation: facilitates interface integrity checks.

Additionally, for the LVDS only, there is the option to set a configurable output drive.

By default, the LVDS interface is selected on power-up and after a reset. As can be seen in Figure 50, for LVDS, the data path of the ADC results is routed though the offset and gain correction block where there is the option for the following:

- ► Continuously read, directly, the raw ADC conversion results.
- ► Continuously read the ADC results processed by a user-selected digital filter (see the [Digital Filter](#page-59-0) section for details).
- ► Read up to 16k unfiltered results from the FIFO.
- ► Read up to 16k digitally filtered results from the FIFO.

![](_page_31_Figure_16.jpeg)

*Figure 50. LVDS Data Interface Options*

If configured for the SPI data interface, as can be seen in Figure 51, the available data paths are as follows:

- ► Read up to 16k unfiltered results from the FIFO.
- ► Read up to 16k digitally filtered results from the FIFO.

![](_page_31_Picture_21.jpeg)

*Figure 51. SPI Data Interface Data Path Options*

Additional features specific to the selected interface format are also available and are described in the [LVDS Data Interface](#page-41-0) section and the [SPI Data Interface](#page-47-0) section.

#### **SPI CONFIGURATION INTERFACE**

All serial transactions between the system host and the AD4086 configuration registers are executed using the configuration SPI. Each serial transaction consists of at least one instruction phase during which the desired memory operation, that is, read or write, and the starting address for the transaction are transmitted to the AD4086. The instruction phase is immediately followed by a data transaction phase during which one or more bytes of information is exchanged between the host and the AD4086. This content is framed by a continuous assertion of the interface chip select (CS ) as illustrated in the generic timing presented in Figure 52 and Figure 53.

![](_page_31_Figure_26.jpeg)

*Figure 52. Generic SPI Configuration Frame, CRC Disabled*

![](_page_31_Figure_28.jpeg)

*Figure 53. Generic SPI Configuration Write Operation, CRC Enabled*

**[analog.com](http://www.analog.com/en/index.html) Rev. 0 | 32 of 91**

# **DIGITAL INTERFACE**

#### **Configuration SPI Timing**

### **Write Data Frame**

![](_page_32_Figure_4.jpeg)

*Figure 54. Configuration SPI Timing, Data Write Frame, 16-Bit Instruction Mode (Default)*

![](_page_32_Figure_6.jpeg)

*Figure 55. Configuration SPI Timing, Data Write Frame, 8-Bit Instruction Mode, Single 8-Bit Register*

![](_page_32_Figure_8.jpeg)

*Figure 56. Configuration SPI Timing, Data Write Frame, 8-Bit Instruction Mode, Streaming Mode, Multibyte Register*

**[analog.com](http://www.analog.com/en/index.html) Rev. 0 | 33 of 91**

# **DIGITAL INTERFACE**

#### **Read Data Frame**

![](_page_33_Figure_3.jpeg)

*Figure 57. Configuration SPI Timing, Data Read Frame, 16-Bit Instruction Mode (Default)*

![](_page_33_Figure_5.jpeg)

*Figure 58. Configuration SPI Timing, Data Read Frame, 8-Bit Instruction Mode*

![](_page_33_Figure_7.jpeg)

*Figure 59. Configuration SPI Timing, Data Read Frame, 8-Bit Instruction Mode, Steaming Mode, Multibyte Register*

**[analog.com](http://www.analog.com/en/index.html) Rev. 0 | 34 of 91**

# **DIGITAL INTERFACE**

![](_page_34_Figure_2.jpeg)

*Figure 60. Configuration SPI Timing, Data Read Frame, Continuous SCLK*

#### **Instruction Phase**

An instruction phase immediately follows the assertion of the CS pin (Logic 0) and is terminated by transmission of a complete instruction packet or deassertion of CS. The instruction packet starts with a single command bit indicating the operation type (Logic 1 for read, and Logic 0 for write) that is then followed by the start address for the operation. By default, the address is 15 bits long, but the data interface has an optional short instruction mode that reduces it to seven bits. The short instruction mode is enabled by setting the SHORT\_INSTRUCTION bit = 1 in the Interface Configuration B register (see the [Interface Configuration B Register](#page-71-0) section, Address 0x01).

#### **Data Phase**

Each instruction phase is immediately followed by an associated data phase, during which data is either shifted out of the serial data output (SDO) on the falling edge of SCLK (read access) or is shifted into the device configuration memory through SDI on the rising edge of SCLK (write access). The minimum size of the data payload is defined as a single byte; however, it can include multiple bytes depending on the depth of the register addressed and the interface configuration settings for the SINGLE\_INST and STRICT\_REGISTER\_ACCESS bits (Register 0x01, Bit 7, and Register 0x10, Bit 5, respectively).

# **Write Access**

When CS is forced low, a new serial instruction phase begins. The first bit sent in the instruction phase is the command bit, and when it is forced low (Logic 0) this indicates a write operation. The command bit is followed by an address that, for the write operation, indicates where the information received in the subsequent data phase will be stored. As previously described in the Instruction Phase section, the address has a default length of 15 bits, but the address can optionally be shortened to seven bits.

Following the instruction phase, an integer number of bytes containing the data payload for one or more registers in the configuration

memory are transmitted to the AD4086. The size of the payload in this data phase is bounded by the selected SINGLE\_INST and STRICT\_REGISTER\_ACCESS interface options as described in the [Strict Access Selection and Multibyte Registers](#page-36-0) section. Each data byte is loaded into the addressed register as it is received, assuming the interface CRC is disabled. If the CRC is enabled, however, the addressed data register is only loaded if the internally computed checksum matches the CRC value received from the host. In the event that the computed CRC and received checksum from the host for a given entity are inconsistent, the register update terminates and all subsequent data in the given frame is treated as invalid as well. The checksum computation for the interface CRC function is described in detail in the [Configuration Cyclical](#page-39-0) [Redundancy Check \(CRC\)](#page-39-0) section.

Note that during the data phase of a write operation, the SDO output is driven to Logic 0 when the product is not reporting the latest CRC checksum to ensure a valid data state is presented to the host controllers SDI pin.

#### **Read Access**

The SPI enables read access to the configuration registers to validate previous configuration writes, read the device identification, or verify the interface status.

When CS is forced low, a new serial instruction phase begins. The first bit sent in the instruction phase is the command bit, and when it is forced high (Logic 1) this indicates a read operation. The command bit is followed by an address that, for the read operation, indicates the start address for the register space to be accessed. As previously described in the Instruction Phase section, the address has a default length of 15 bits, but the address can optionally be shortened to seven bits.

During the subsequent data phase, content from the addressed register space is shifted out, MSB first, on the SDO line on the falling edge of SCLK. The number of bytes transmitted in any one data frame is determined by the interface configuration setting selections for the SHORT\_INSTRUCTION and STRICT\_REG-

**[analog.com](http://www.analog.com/en/index.html) Rev. 0 | 35 of 91**

#### <span id="page-35-0"></span>**DIGITAL INTERFACE**

ISTER\_ACCESS options as demonstrated in the examples shown in the Instruction Mode Selection section and the [Strict Access](#page-36-0) [Selection and Multibyte Registers](#page-36-0) section.

#### **Instruction Mode Selection**

The configuration interface memory controller defaults to streaming mode upon power up (SINGLE\_INST = 0). In streaming mode, multiple, contiguous registers are accessed in a single SPI frame, starting at the address specified in the instruction phase. In streaming mode, only one instruction phase is permitted per SPI frame, requiring a new SPI frame be initiated for changing access commands or otherwise access a noncontiguous address in the register space. For each byte transferred during the subsequent data phase, the internal address counter is automatically updated according to the setting of the ADDR\_ASCENSION bit in the Interface Configuration A register (see the [Interface Configuration A Register](#page-70-0) section), in the way specified by Table 15.

*Table 15. Address Ascension Selection*

| ADDR_ASCENSION Bit<br>Value | Address Controller Behavior<br>(STRICT_REGISTER_ACCESS = 1)                                              |
|-----------------------------|----------------------------------------------------------------------------------------------------------|
| 0 (Default)                 | Decrement Address. Multibyte registers are accessed<br>by addressing the most significant byte address.  |
| 1                           | Increment Address. Multibyte registers are accessed<br>by addressing the least significant byte address. |

Figure 61 illustrates the generic SPI frame formatting for a serial transaction using the default interface configuration. In this example, a portion of the configuration register space consisting of a byte-wide register and a multibyte register is accessed. The address for the byte-wide register resides in the most significant address (ADDRESS) and the most significant byte of the multibyte register resides in the least significant address of the register segment. By default, the ADDR\_ASCENSION property is set to descending, indicating that the address for the most significant register is passed to the host controller during the instruction phase. Depending on the selected operation, the instruction word is followed by either a payload consisting of data for the byte-wide register (DATA), least significant (LSBYTE), and most significant bytes (MSBYTE) of the multibyte register, or, in the case of a read access, padding bits. As a convention, it is recommended to pass Logic 1 to SDI during a read access to avoid accidentally addressing address zero for write access.

In single instruction mode (SINGLE\_INST = 1), the memory access controller requires an instruction phase to transmit for each register accessed in a given SPI frame as illustrated in Figure 62. This mode is useful when access to nonadjacent sections of the register space is required in a given SPI frame. Note that, the same access flexibility can be achieved in stream mode by initiating a new SPI frame for each unique register access.

The single instruction mode is selected by setting SINGLE\_INST = 1 in the Interface Configuration B register (see the [Interface](#page-71-0) [Configuration B Register](#page-71-0) section, Address 0x01).

![](_page_35_Figure_11.jpeg)

*Figure 61. Interface Access Example, Default Interface Configuration, Streaming Mode (ADDR\_ASCENSION = 0)*

![](_page_35_Figure_13.jpeg)

*Figure 62. Interface Access Example, Single Instruction Mode (SINGLE\_INST = 1), All Other Interface Options Default*

**[analog.com](http://www.analog.com/en/index.html) Rev. 0 | 36 of 91**

#### <span id="page-36-0"></span>**DIGITAL INTERFACE**

# **Address Ascension Selection**

The address ascension selection (ADDR\_ASCENSION) bit, as described in previous sections, determines how the internal interface address pointer is updated for each byte of data transmitted to the AD4086 in streaming mode (SINGLE\_INST = 0). If using single instruction mode (SINGLE\_INST = 1), each register is directly addressed through its own instruction phase as illustrated in [Figure](#page-35-0) [62](#page-35-0), and thus, the address pointer is not updated. Regardless of the setting for SINGLE\_INST, the ADDR\_ASCENSION bit directly impacts the formatting of the SPI frame in terms of selection of the instruction phase starting address and byte order of the data phase payload. This impact is described in greater detail in the Strict Access Selection and Multibyte Registers section as much of the data formatting is dependent on this interface configuration selection. The ADDR\_ASCENSION selection bit is located in the Interface Configuration A register (see the [Interface Configuration A](#page-70-0) [Register](#page-70-0) section, Address 0x00).

As summarized in [Table 15,](#page-35-0) the ADDR\_ASCENSION bit is cleared by default, resulting in the address pointer decrementing by one for each data byte transmitted. In this decrement configuration (ADDR\_ASCENSION = 0), the address pointer decrements from the starting address indicated in the instruction phase by one for each data phase byte received until the counter reaches Address 0x0000. If additional bytes are received, the pointer automatically rolls over to the maximum address value, 0x7FFF; the rollover behavior is fixed, and therefore, independent of the SHORT\_IN-STRUCTION value or the physical address space occupied by the user configurable registers. It is important to understand this behavior to avoid generating interface errors associated with attempting to access one or more invalid register addresses. Limit register access to the register address space associated with the device configuration as described in the [Configuration Registers](#page-68-0) section.

Alternatively, the ADDR\_ASCENSION bit can be set (ADDR\_AS-CENSION = 1), resulting in the address pointer incrementing by one, starting at the address identified in the instruction word, for each data phase byte received at the AD4086 in a given SPI frame. In a manner similar to the descending case, the address counter continues to increment for each data byte received until the maximum address value, 0x7FFFF, is reached, after which the pointer rolls over to 0x0000.

# **Strict Access Selection and Multibyte Registers**

Several locations in the AD4086 configuration memory have been assigned as multibyte registers to support the storage requirements. For example, the offset correct register (see the [Offset](#page-87-0) [Correction Register](#page-87-0) section, Address 0x25) and gain correction register (see the [Gain Correction Register](#page-88-0) section, Address 0x27) are multibyte registers because the resolution of the correction coefficients they contain exceeds a single byte. For a complete listing of multibyte registers, refer to the [Configuration Registers](#page-68-0)

section. The length of each register, in bytes, is captured in [Table](#page-68-0) [31](#page-68-0) in addition to other characteristic information.

The function of the STRICT\_REGISTER\_ACCESS bit is to indicate to the interface controller that all bytes of a multibyte register must be accessed in the current frame for valid communication to have occurred. In the event a multibyte register is only partially accessed, an interface fault is generated in the Interface Status A register (see the [Interface Status A Register](#page-77-0) section, Address 0x11), and the partial content update is discarded. The intent of this restriction is to ensure that corresponding configuration quantities are updated in a manner that produces the desired device operation. The access restriction function is enabled by default (STRICT\_REGIS-TER\_ACCESS = 1) and can be disabled by clearing the access bit (STRICT\_REGISTER\_ACCESS = 0) in the Interface Configuration C register (see the [Interface Configuration C Register](#page-76-0) section, Address 0x10). With register access restriction disabled, each byte of the configuration memory can be independently addressed; however, it is then incumbent on the software to correctly configure any multibyte registers in the device memory to achieve the desired behavior.

The decision to enable or disable the register access restriction has implications with regards to the correct construction of the SPI frames containing one or more multibyte register accesses. When STRICT\_REGISTER\_ACCESS is disabled, each byte of a multibyte register is treated as a singular element. Furthermore, the interface does not indicate a fault if all bytes of the register are not programmed, or if the bytes are programmed in a random order, and therefore, it is incumbent on the host to ensure that the content of those registers are updated in a manner that produces the desired function in the device.

When STRICT\_REGISTER\_ACCESS is enabled, specific access rules are enforced to ensure consistency between the data and the expected behavior of the device. To understand how these rules apply to multibyte registers in the configuration memory, it is important to understand how the memory is organized. By convention, multibyte registers are arranged in the configuration memory such that the most significant byte of the register is stored in the most significant address of the assigned register space as illustrated in [Figure 63.](#page-37-0) As a result, the byte order of the register content transmitted in the data phase is dependent on the ADDR\_ASCENSION selection.

**[analog.com](http://www.analog.com/en/index.html) Rev. 0 | 37 of 91**

# <span id="page-37-0"></span>**DIGITAL INTERFACE**

![](_page_37_Figure_2.jpeg)

*Figure 63. Generic Byte Wide Memory, Multibyte Register Example*

As indicated in Figure 64, the address counter, by default, automatically decrements (ADDR\_ASCENSION = 0) such that the most significant byte of the multibyte register is accessed first, followed

by the remaining byte(s) in that register in ascending order. Conversely, if ADDR\_ASCENSION = 1, the least significant byte of the multibyte register is accessed first followed by most significant byte.

As an extension of this concept, when STRICT\_REGISTER\_AC-CESS = 1, any SPI frame that accesses a multibyte register as the first entity in the data transfer must correctly set the starting address in the instruction word to correspond to the ADDR\_AS-CENSION selection. In the case that the address counter automatically decrements (ADDR\_ASCENSION = 0), the starting address is assigned to the register address for the least significant byte of that multibyte register, and conversely, if configured to increment automatically, the starting address must be set to the register address for the most significant byte. As a result of the change to ADDR\_ASCENSION from automatic address decrement (0) to automatic increment (1), [Figure 61](#page-35-0) and [Figure 62](#page-35-0) will change as illustrated in Figure 64 and Figure 65 to accommodate the changes in data phase byte order and instruction phase multibyte register start address.

![](_page_37_Figure_7.jpeg)

*Figure 64. Single Instruction Format, ADDR\_ASCENSION = 0 (Descend), STRICT\_REGISTER\_ACCESS = 1 (Enabled)*

![](_page_37_Figure_9.jpeg)

*Figure 65. Single Instruction Format, ADDR\_ASCENSION = 1 (Increment), STRICT\_REGISTER\_ACCESS = 1 (Enabled)*

**[analog.com](http://www.analog.com/en/index.html) Rev. 0 | 38 of 91**

# <span id="page-38-0"></span>**DIGITAL INTERFACE**

#### **Status Data Transmission**

The Interface Status A register (see the [Interface Status A Reg](#page-77-0)[ister](#page-77-0) section, Address 0x11) and device status register (see the [Device Status Register](#page-78-0) section, Address 0x14) contain status data pertaining to the communications interface and the device itself, respectively. This data enables troubleshooting of device configuration during development and also provides continuous coverage of potential communication issues between the host and the interface once deployed. The SPI controller can access the data through regular register read operations. However, the AD4086 can be configured to autonomously transmit status data through the SDO line every time while the SPI controller is sending the SPI instruction

phase data over the SDI. This feature is controlled through the SEND\_STATUS bit in the Interface Configuration C register (see the [Interface Configuration C Register](#page-76-0) section, Address 0x10), and it is disabled by default. To enable this bit, set SEND\_STATUS = 1. The status data that is sent is taken from the Interface Status A register and from the device status register, but the content is different depending on the setting of the SHORT\_INSTRUCTION bit in the Interface Configuration B register (see the [Interface Configuration](#page-71-0) [B Register](#page-71-0) section. (Note that the length of the instruction phase also depends on this setting). See Table 16 and [Table 17](#page-39-0) for a description of the status data sent in each case, where the status data is sent MSB first.

*Table 16. Device Status Data Sent Through the SDO in Long Instruction Mode (SHORT\_INSTRUCTION = 0)*

| Bit | Name            | Description                                                                                                                                                                                                                                                                                                                            |
|-----|-----------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 15  | Not applicable  | Bit 15 is always 0.                                                                                                                                                                                                                                                                                                                    |
| 14  | Not applicable  | Bit 14 is always 0.                                                                                                                                                                                                                                                                                                                    |
| 13  | FIFO_FULL       | Device Status Register Bit 7: FIFO Full Status Flag.                                                                                                                                                                                                                                                                                   |
|     |                 | 0: FIFO Not Full.                                                                                                                                                                                                                                                                                                                      |
|     |                 | 1: FIFO Full.                                                                                                                                                                                                                                                                                                                          |
| 12  | FIFO_READ_DONE  | Device Status Register Bit 6: FIFO Read Done Flag.                                                                                                                                                                                                                                                                                     |
|     |                 | 0: FIFO Read Not Done.                                                                                                                                                                                                                                                                                                                 |
|     |                 | 1: FIFO Read Done.                                                                                                                                                                                                                                                                                                                     |
| 11  | HI_STATUS       | Device Status Register Bit 5: High Threshold Detection Status Flag.                                                                                                                                                                                                                                                                    |
|     |                 | 0: High Threshold Event Not Detected.                                                                                                                                                                                                                                                                                                  |
|     |                 | 1: High Threshold Event Detected.                                                                                                                                                                                                                                                                                                      |
| 10  | LO_STATUS       | Device Status Register Bit 4: Low Threshold Detection Status Flag.                                                                                                                                                                                                                                                                     |
|     |                 | 0: Low Threshold Event Not Detected.                                                                                                                                                                                                                                                                                                   |
|     |                 | 1: Low Threshold Event Detected.                                                                                                                                                                                                                                                                                                       |
| 9   | ADC_CNV_ERR     | Device Status Register Bit 2: ADC Conversion Error Flag.                                                                                                                                                                                                                                                                               |
|     |                 | 0: ADC Conversion OK.                                                                                                                                                                                                                                                                                                                  |
|     |                 | 1: ADC Conversion Error. A. Conversion period is lower than minimum value for speed grade. B. DSP error.                                                                                                                                                                                                                               |
| 8   | ROM_CRC_ERR     | Device Status Register Bit 1: Read Only Memory (ROM) CRC and/or Error Correction Code (ECC) Failure Flag.                                                                                                                                                                                                                              |
|     |                 | 0: ROM CRC Check OK.                                                                                                                                                                                                                                                                                                                   |
|     |                 | 1: ROM CRC and/or ECC Failure.                                                                                                                                                                                                                                                                                                         |
| 7   | POR_ANA_FLAG    | Device Status Register Bit 3: POR Analog Status. Allows user to detect when an analog POR event has occurred. An analog POR<br>is triggered at power-up or when the logic supply drops to less than some threshold value, when the ADC reference drops to less<br>than some threshold value, or when the user issues a software reset. |
|     |                 | 0: Analog POR Flag Cleared.                                                                                                                                                                                                                                                                                                            |
|     |                 | 1: Analog POR Event Detected.                                                                                                                                                                                                                                                                                                          |
| 6   | POR_FLAG        | Device Status Register Bit 0: POR Status. Allows user to detect when a POR event has occurred. A POR is triggered at power-up                                                                                                                                                                                                          |
|     |                 | or when the logic supply drops to less than some threshold value or when the user issues a software reset.                                                                                                                                                                                                                             |
|     |                 | 0: POR Flag Cleared.                                                                                                                                                                                                                                                                                                                   |
|     |                 | 1: POR Event Detected.                                                                                                                                                                                                                                                                                                                 |
| 5   | NOT_READY_ERR   | Interface Status A Register Bit 7: Device Not Ready for Transaction. This bit is set if the user attempts to execute an SPI<br>transaction before the completion of digital initialization.                                                                                                                                            |
| 4   | CLOCK_COUNT_ERR | Interface Status A Register Bit 4: Clock Count Error. This bit is set when an incorrect number of clocks is detected in a transaction.                                                                                                                                                                                                 |
| 3   | CRC_ERR         | Interface Status A Register Bit 3: CRC Error. This bit is set when the SPI controller does not send a CRC value or when the CRC<br>value calculated by the device does not match the value received from the SPI controller.                                                                                                           |

**[analog.com](http://www.analog.com/en/index.html) Rev. 0 | 39 of 91**

### <span id="page-39-0"></span>**DIGITAL INTERFACE**

*Table 16. Device Status Data Sent Through the SDO in Long Instruction Mode (SHORT\_INSTRUCTION = 0) (Continued)*

| Bit | Name                            | Description                                                                                                                                                                                                                                                |
|-----|---------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 2   | WR_TO_RD_ONLY_REG_ERR           | Interface Status A Register Bit 2: Write to Read Only Register Error. Write to Read Only Register Attempted. This bit is set when<br>the user attempts a write to a register that is read-only.                                                            |
| 1   | REGISTER_PARTIAL_<br>ACCESS_ERR | Interface Status A Register Bit 1: Register Partial Access Error. This bit is set when a fewer than expected number of bytes are<br>read from or written to in a multibyte register access. This bit is only valid when strict register access is enabled. |
| 0   | ADDRESS_INVALID_ERR             | Interface Status A Register Bit 0: Invalid Address Error. Attempt to read or write nonexistent register address. This bit is set when<br>the user tries to access register addresses outside the allowed memory map space.                                 |

*Table 17. Device Status Data Sent Through the SDO in Short Instruction Mode (SHORT\_INSTRUCTION = 1)*

| Bit | Name                            | Description                                                                                                                                                                                                                                                |
|-----|---------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 7   | Not applicable                  | Bit 7 is always 0.                                                                                                                                                                                                                                         |
| 6   | POR_FLAG                        | Device Status Register Bit 0: POR Status. Allows user to detect when a POR event has occurred. A POR is triggered at power-up<br>or when the logic supply drops to less than some threshold value or when the user issues a software reset.                |
|     |                                 | 0: POR Flag Cleared.                                                                                                                                                                                                                                       |
|     |                                 | 1: POR Event Detected.                                                                                                                                                                                                                                     |
| 5   | NOT_READY_ERR                   | Interface Status A Register Bit 7: Device Not Ready For Transaction Error. This bit is set if the user attempts to execute an SPI<br>transaction before the completion of digital initialization.                                                          |
| 4   | CLOCK_COUNT_ERR                 | Interface Status A Register Bit 4: Clock Count Error. This bit is set when an incorrect number of clocks is detected in a transaction.                                                                                                                     |
| 3   | CRC_ERR                         | Interface Status A Register Bit 3: CRC Error. This bit is set when the SPI controller does not send a CRC, or when the CRC value<br>calculated by the device does not match the value sent by the SPI controller.                                          |
| 2   | WR_TO_RD_ONLY_REG_ERR           | Interface Status A Register Bit 2: Write To Read-only Register Error. This bit is set when the user attempts a write to a register that<br>is read only.                                                                                                   |
| 1   | REGISTER_PARTIAL_<br>ACCESS_ERR | Interface Status A Register Bit 1: Register Partial Access Error. This bit is set when a fewer than expected number of bytes are<br>read from or written to in a multibyte register access. This bit is only valid when strict register access is enabled. |
| 0   | ADDRESS_INVALID_ERR             | Interface Status A Register Bit 0: Invalid Address Error. This bit is set when the user tries to read from or write to a register<br>address outside the allowed memory map space.                                                                         |

# **Configuration Cyclical Redundancy Check (CRC)**

The AD4086 includes optional configuration error detection based on an 8-bit cyclical redundancy check algorithm. When enabled, an 8-bit checksum is inserted into the serial data output stream (SDO) during the data phase after each complete register transaction. Depending on the register access type,that is, read or write, the host is expected to conditionally provide a corresponding checksum to the SDI immediately following each register access. The interface controller uses the host supplied checksum to determine if a CRC error has occurred.

A mismatch in the checksum values computed by the host and the AD4086 interface results in setting the CRC\_ERR flag (CRC\_ERR = 1) in the Interface Status A register (see the [Interface Status](#page-77-0) [A Register](#page-77-0) section, Address 0x11). During a write access, a CRC error invalidates the most recent register data as well as any subsequent register data writes if in streaming mode (SINGLE\_INST = 0), which prevents loading any potentially corrupted data into the configuration memory. In response to a CRC event, the host controller is required to initiate a new SPI frame to retry configuration of the effected memory locations. In the event the CRC\_ERR is detected during a data read, the host controller must discard

the received data and retry the data read in a new SPI frame. Clear the CRC\_ERR flag before any attempt to initiate a repeated read or write to the configuration memory to allow detection of any subsequent errors. The error flag is cleared by writing code 0x08 to the Interface Status A register to set the CRC\_ERR bit to a Logic 1. It is recommended that an immediate read of the Interface Status A register follows any attempt to clear the fault to validate the attempt was successful.

The configuration CRC function is disabled by default and can be enabled through two complementary bit fields, CRC\_ENABLE and CRC\_ENABLEB, in the Interface Configuration C register (see the [Interface Configuration C Register](#page-76-0) section, Address 0x10). To enable the CRC function, set the CRC\_ENABLE bits to 1 and the CRC\_ENABLEB bits to 10. Each of the complementary CRC bit fields is 2-bit wide, and any combination other than that specified results in the function remaining disabled. It is important to note that once the CRC function is enabled, a valid checksum from the host controller is required for all subsequent serial transactions according to the conditions described in [Table 18.](#page-40-0) If used, enable and validate the CRC function before writing to any of the device configuration registers. To validate the CRC function is enabled, follow the CRC configuration write with a SPI frame consisting of a read of both the Interface Configuration C register and the Interface

**[analog.com](http://www.analog.com/en/index.html) Rev. 0 | 40 of 91**

#### <span id="page-40-0"></span>**DIGITAL INTERFACE**

Status A register using a valid checksum for the read transaction. If enabled, the register contents for the CRC\_ENABLE and CRC\_EN-ABLEB bits must be 1 and 10, respectively, and the CRC\_ERR bit in the Interface Status A register remains cleared (Logic 0). Once confirmed, proceed with programming the remaining configuration registers.

*Table 18. Host Controller (SDI) Conditional Checksum Requirement Summary*

| Command | SINGLE_INST Bit Value                      | Check Sum Requirement                                                    |
|---------|--------------------------------------------|--------------------------------------------------------------------------|
| Write   | Streaming (0) or single<br>instruction (1) | After each data register payload                                         |
| Read    | Streaming (0)                              | After the first register data payload<br>following the instruction phase |
|         | Single instruction (1)                     | After each data register payload                                         |

The following CRC-8 polynomial is implemented in the AD4086 to compute the checksum for each register transaction:

$$x^8 + x^2 + x + 1$$

Each serial transaction is processed through this polynomial to generate the checksum on a per register basis. The data and seed values used for each checksum calculation are a function of the access command (read/write); ADDR\_ASCENSION, STRICT\_REG-ISTER\_ACCESS, and SINGLE\_INST settings; and the location of the register data in the data stream as summarized in Table 19.

All register write access operations, regardless of SINGLE\_INST setting, require a valid CRC checksum to be sent from the host following the data payload for each register. For multibyte registers, if STRICT\_REGISTER\_ACCESS = 1, a valid CRC is appended to the data stream after all bytes of the addressed register are sent. If STRICT\_REGISTER\_ACCESS is cleared (0), each byte transmitted must be followed by a valid checksum using the computation rules that are described as follows.

For read access, the computation and transmission of a valid checksum from the host is required to validate the command and starting address only. In streaming mode (SINGLE\_INST = 0), a CRC checksum is sent from the host controller after the first register data payload only. Fill all subsequent register accesses in streaming mode with padding data. The AD4086 continues to produce valid checksum values after each register read to allow validation in the host using the preceding data. As a new instruction phase is required for each register accessed in single instruction mode, a valid host CRC checksum is required for each register accessed.

In single instruction mode (SINGLE\_INST = 1), the polynomial is computed for each register using the default seed value of 0xA5, the instruction phase data, and depending on the access command, the desired register or padding data. In streaming mode (SINGLE\_INST = 0), the checksum computation for the first register in the data stream is computed as if single instruction mode were selected. Each subsequent register access checksum computation is seeded with the starting address for the current register and the corresponding data. Note that the starting address for multibyte registers changes with the ADDR\_ASCENSION selection, assuming the register access restriction is enabled (STRICT\_REGISTER\_AC-CESS = 1). As previously described, the memory convention dictates that if ADDR\_ASCENSION is set to 0, the address for the least significant byte of the multibyte register serves as the starting address. Conversely, if the ADDR\_ASCENSION bit is set to 1, the address of the most significant byte of the multibyte register is used.

*Table 19. Configuration CRC Checksum Source Data Summary vs. SINGLE\_INST and SPI Command*

| Single Instruction Mode (SINGLE_INST = 1) or<br>Streaming Mode First CRC<br>Streaming Mode (SINGLE_INST = 0) after first CRC<br>Checksum |            |                                  |      |               |                                 |
|------------------------------------------------------------------------------------------------------------------------------------------|------------|----------------------------------|------|---------------|---------------------------------|
| Command                                                                                                                                  | Source     | Data Source                      | Seed | Data Source   | Seed                            |
| Write                                                                                                                                    | Controller | Instruction and data             | 0xA5 | Register data | Current start address           |
|                                                                                                                                          | AD4086     | Instruction and data             |      | Register data | Current start address           |
| Read                                                                                                                                     | Controller | Instruction and padding data     | 0xA5 |               | Not required, send padding data |
|                                                                                                                                          | AD4086     | Instruction and register content |      | Register data | Current start address           |

![](_page_40_Figure_14.jpeg)

*Figure 66. Streaming Mode Configuration with CRC Enabled, ADDR\_ASCENSION = 1*

**[analog.com](http://www.analog.com/en/index.html) Rev. 0 | 41 of 91**

# <span id="page-41-0"></span>**DIGITAL INTERFACE**

![](_page_41_Figure_2.jpeg)

*Figure 67. Single Instruction Mode Configuration with CRC Enabled, ADDR\_ASCENSION = 1*

![](_page_41_Figure_4.jpeg)

*Figure 68. Streaming Mode Configuration with CRC Enabled, STRICT\_REGISTER\_ACCESS = 0 (Disabled) , ADDR\_ASCENSION = 0*

#### **LVDS DATA INTERFACE**

# **LVDS Data Interface Configuration**

The LVDS interface consists of up to five pairs of differential signals. The data clock input pair (CLK+ and CLK−), echoed data clock output pair (DCO+ and DCO−), two data output lanes (DA+ and DA− , DB+ and DB− ), and optionally, the conversion clock can be configured as either an LVDS pair (CNV+ and CNV−) or as a CMOS using CNV+, where for this case, CNV− is connected to GND. This user selection is configured using the LVDS\_CNV\_EN bit in the ADC Data Interface Configuration B register (see the [ADC](#page-80-0) [Data Interface Configuration B Register](#page-80-0) section, Address 0x16). The data lanes use a DDR scheme, and each scheme can support a throughput of up to 560 (Mbps). By default, LVDS is selected as the primary data interface for accessing conversion results.

To achieve maximum throughput, it is necessary that while a conversion is performed the result of the previous conversion is read. For this reason, it is critical that both the rising and falling edges of CNV+ and CNV− are closely time aligned to the rising edge of CLK+ and CLK−. To avoid introducing noise into the conversion result, the CLK+ and CLK− edge placement must be aligned to within ±535ps (tCCA) of the interface clock (CLK±), as specified in [Table 2](#page-5-0).

The data interface is highly configurable allowing the customization of the output stream to meet a wide range of applications. Configuration options include the number of active lanes (1, 2), self clocked and echo clock modes, interface test functions, and data encoding. LVDS interface mode is used in applications where continuous conversion at rates exceeding 1MHz is required.

Transmission of the result data occurs MSB first and is output after the amount of time specified in detail in the [ADC Result Latency](#page-44-0) [and LVDS Interface Alignment](#page-44-0) section.

#### **LVDS Active Data Lane Count**

The LVDS interface can be configured to output the result data on either one or two data lanes, which is controlled by the SPI\_LVDS\_LANES bit in the ADC Data Interface Configuration A register (see the [ADC Data Interface Configuration A Register](#page-79-0) section, Address 0x15). By default, this bit is set to 0 (one lane active), and setting SPI\_LVDS\_LANES = 1 uses two data lanes. Note that this bit is also used to configure the number of active data lanes for the SPI.

In single lane operation, Data Lane DA+ and Data Lane DA− is enabled as the primary data output, and the conversion result is shifted out serially, MSB first, using 7 interface clocks applied to CLK+ and CLK− inputs per conversion. The result data is shifted out of the device on each edge of the echo clock outputs, DCO+ and DCO−. The result MSB (D13) and all odd numbered data bits are output on the falling edge of the interface clock. Conversely, the even numbered data bits are output on the rising edge of the interface clock.

In dual lane configuration, the result data is shifted out in parallel, two bits per clock edge, MSBs first. As a result, only 4 interface clocks are required per conversion. As the data access period is equivalent to the conversion period, the interface clock frequency is reduced by a factor of two relative to the single lane case. As a consequence of the increased interface clock period, see the [ADC](#page-44-0) [Result Latency and LVDS Interface Alignment](#page-44-0) section for the timing and latency implications on both the single lane and dual lane count configurations.

**[analog.com](http://www.analog.com/en/index.html) Rev. 0 | 42 of 91**

# <span id="page-42-0"></span>**DIGITAL INTERFACE**

#### **Echo Clock Mode**

In LVDS data interface mode, the DCO+ and DCO− pin pair is an echo clock output that provides a buffered and delayed version of CLK+ and CLK− pin pair, facilitating data clocking to the host controller data clocking. This feature is controlled by the LVDS\_SELF\_CLK\_MODE bit in the ADC Data Interface Configuration B register (see the [ADC Data Interface Configuration B Regis](#page-80-0)[ter s](#page-80-0)ection, Address 0x16). By default, echo clock mode is active (LVDS\_SELF\_CLK\_MODE = 0). Setting LVDS\_SELF\_CLK\_MODE = 1 disables the DCO+ and DCO− output driver, putting the device in self clock mode (see the [Self Clock Mode](#page-43-0) section) .

When echo clock mode is active, the interface requires a minimum of three LVDS pairs (CLK+ and CLK−, DCO+ and DCO−, and DA+ and DA−) to be connected between the host controller and the AD4086. A maximum of five LVDS pairs are required if the CNV+ and CNV− pin pair is configured as an LVDS input and the DB+ and DB− data lane is enabled. The conversion clock (CNV+ and CNV−) and data clock (CLK+ and CLK−) can be shared amongst multiple AD4086 devices as long as care is taken to fanout the clock network, such that the edge placement requirement is satisfied.

In echo clock mode, data from enabled lanes is clocked out in sync to both rising and falling edges of DCO+ and DCO− in a DDR scheme. Figure 69 and Figure 70 illustrate the relevant LVDS interface timing with respect to the DCO+ and DCO− echo clock for single lane and dual lane configurations, respectively. Calculation of tMSB\_READ is described in the [ADC Result Latency and LVDS](#page-44-0) [Interface Alignment](#page-44-0) section.

Consider matching the data clock (DCO+ and DCO−) and data lane (DA+ and DA−, DB+ and DB−) lane routing from the ADC to the host processor for the physical layout to minimize timing skew, which may affect data recovery in the host. For additional routing suggestions, see the [Layout Guidelines](#page-67-0) section.

![](_page_42_Figure_8.jpeg)

*Figure 69. Continuous Conversion Timing, LVDS Data Interface, Single Data Lane, Echo Clock Mode*

![](_page_42_Figure_10.jpeg)

*Figure 70. Continuous Conversion Timing, LVDS Data Interface, Dual Data Lane, Echo Clock Mode*

**[analog.com](http://www.analog.com/en/index.html) Rev. 0 | 43 of 91**

# <span id="page-43-0"></span>**DIGITAL INTERFACE**

# **Self Clock Mode**

In LVDS data interface mode, it is possible to disable the DCO+ and DCO− echo clock output (see the [Echo Clock Mode](#page-42-0) section) by setting LVDS\_SELF\_CLK\_MODE = 1 in the ADC Data Interface Configuration B register (see the [ADC Data Interface Configuration](#page-80-0) [B Register s](#page-80-0)ection, Address 0x16). This setting puts the device in self clock mode disabling the DCO+ and DCO− output driver, with the benefit of saving interface power as well as reducing the

number of LVDS pairs required to interface with the host controller. In this mode, the DCO+ and DCO− pins can be left disconnected; therefore, in single-lane configurations, a minimum of two LVDS pairs (CLK+ and CLK−, DA+ and DA−) are required to connect to each AD4086 instance. The interface connectivity can further be simplified by sharing the interface clock (CLK+ and CLK−) between multiple AD4086 instances.

![](_page_43_Figure_5.jpeg)

*Figure 71. Continuous Conversion Timing, LVDS Data Interface, Single Data Lane, Self Clock Mode*

![](_page_43_Figure_7.jpeg)

*Figure 72. Continuous Conversion Timing, LVDS Data Interface, Dual Data Lane, Self Clock Mode*

**[analog.com](http://www.analog.com/en/index.html) Rev. 0 | 44 of 91**

#### <span id="page-44-0"></span>**DIGITAL INTERFACE**

#### **LVDS Manchester Encoding Mode**

This mode is accessed via the ADC\_DATA\_INTF\_CONFIG\_B register (Address 0x16), which produces Manchester encoding of the result data in compliance with IEEE 802.3. This mode can be used in isolated data applications where the converter supplies can be floated and the data outputs capacitively coupled to the host controller. By ensuring that the mean output of each data lane is 0, the receiver side common-mode voltage is not disturbed by the result pattern.

Manchester encoding is available in dual lane LVDS mode only so that the maximum data throughput is achievable with the maximum 280MHz LVDS clock rate.

Figure 73 shows an example how this isolation can be implemented. Note that the LVDS 100Ω termination resistor prior to the isolation capacitors is required.

![](_page_44_Picture_6.jpeg)

*Figure 73. Isolated LVDS*

# **ADC Result Latency and LVDS Interface Alignment**

When AD4086 is configured for LVDS interface mode, each conversion result is placed into the LVDS interface output shift register(s). The LVDS\_CNV\_CLK\_CNT bits in the ADC Data Interface Configuration B register (see the [ADC Data Interface Configuration B](#page-80-0) [Register s](#page-80-0)ection, Address 0x16) is used to configure the point in time when the conversion result data is loaded into the LVDS interface output shift register(s). The total time from the rising edge of a convert pulse to when the MSB of that conversion request is internally available to transfer to the output register is defined as (tCYC + tMSB), both specified in [Table 2](#page-5-0). Because the transfer of this result data is under the control of the LVDS of CLK+ and CLK−, there is an additional (1.5 × tCLK) that must be allowed to guarantee a fully completed result is transferred to the interface for read back. The user must calculate the correct required LVDS\_CNV\_CLK\_CNT value and configure the ADC Data Interface Configuration B register (see the [ADC Data Interface](#page-80-0) [Configuration B Register](#page-80-0) section) according to the conversion rate and tCLK used.

For minimum latency, the correct LVDS\_CNV\_CLK\_CNT value to use for a particular conversion rate is calculated as (tMSB/tCLK + 1.5). This number is rounded down to the nearest integer value.

The maximum tMSB time is specified as 22.4ns with gain error correction enabled (see the [Gain Error Correction](https://ccms.web.analog.com/oxygen-webapp/app/Keyref%20tdi1697028251825) section). For a 40MSPS conversion rate in single lane LVDS with a 280MHz LVDS clock, this is calculated as 22.4ns/3.571ns + 1.5, yielding a setting of 7 for the LVDS\_CNV\_CLK\_CNT. Conversion latency is then determined as time, aligned to the falling edge of the CLK signal, described as tMSB\_READ or latency in the timing diagram, which can be calculated as (LVDS\_CNV\_CLK\_CNT + 0.5) × tCLK. For the given example, the single lane latency is calculated as (7+ 0.5) × 3.571ns + tCYC =51.78ns latency.

Taking a dual lane example, the same formula is used, again taking a 40MSPS example, again with gain error correction enabled, the LVDS clock runs at 160MHz and yields ( 22.4ns/6.25ns) + 1.5, resulting in an LVDS\_CNV\_CLK\_CNT of 5, and a total result latency of (5 + 0.5) × 6.25ns + tCYC = 59.37ns latency.

With the gain error correction disabled (see the [Gain Error Correc](https://ccms.web.analog.com/oxygen-webapp/app/Keyref%20tdi1697028251825)[tion](https://ccms.web.analog.com/oxygen-webapp/app/Keyref%20tdi1697028251825) section), the maximum tMSB time is specified as 18ns. For a 40MSPS conversion rate in single lane LVDS with a 280MHz LVDS clock, this is calculated as (18ns/3.571ns) + 1.5, yielding a setting of 6 for the LVDS\_CNV\_CLK\_CNT. Conversion latency is then determined as time, aligned to the falling edge of the CLK signal, described as tMSB\_READ or latency in the timing diagram, which can be calculated as (LVDS\_CNV\_CLK\_CNT + 0.5) × tCLK. For the given example, the single lane latency is calculated as (6 + 0.5) × 3.571 + tCYC = 48.21ns latency.

Using this example, the same formula is used, again taking a dual lane 40MSPS example, the LVDS clock runs at 160MHz and yields (18ns/6.25ns) + 1.5, resulting in an LVDS\_CNV\_CLK\_CNT of 4 and a total result latency of (4 + 0.5) × 3.571ns + tCYC = 53.12ns latency.

Both of these examples are calculated to achieve the minimum latency, and it is possible to use a higher LVDS\_CNV\_CLK\_CNT value, whereby latency is increased by tCLK for each +1 unit increase in the LVDS\_CNV\_CLK\_CNT value.

[Figure 74](#page-45-0) and [Figure 75](#page-45-0) serve as aids to describe the placement of the ADC result data onto the LVDS interface controlled by the LVDS\_CNV\_CLK\_CNT. [Figure 74](#page-45-0) shows that a new result is internally completed after (tCYC + tMSB), and this result is now available to the interface, signified here also by a notional tMSB\_AVAILABLE (introduced only for the purposes of the [Figure 74](#page-45-0) explanation). As this example represents a 40MSPS conversion rate, [Figure 74](#page-45-0) shows that the LVDS\_CNV\_CLK\_CNT setting of 7 is the earliest the conversion result can be loaded to the LVDS interface. One additional full tCLK cycle is required (a complete cycle being CLK+ falling edge to next CLK+ falling edge) is required to move the MSB to the output. This cycle is highlighted within [Figure 74](#page-45-0) also with a notional tMSB\_READ indicator for illustrative purposes only.

**[analog.com](http://www.analog.com/en/index.html) Rev. 0 | 45 of 91**

# <span id="page-45-0"></span>**DIGITAL INTERFACE**

![](_page_45_Figure_2.jpeg)

*Figure 74. Single Lane LVDS, Echo Clock Mode, LVDS\_CNV\_CLK\_CNT Position Example*

![](_page_45_Figure_4.jpeg)

*Figure 75. Dual Lane LVDS, Echo Clock Mode, LVDS\_CNV\_CLK\_CNT Position Example*

**[analog.com](http://www.analog.com/en/index.html) Rev. 0 | 46 of 91**

#### **DIGITAL INTERFACE**

*Table 20. Valid LVDS\_CNV\_CLK\_CNT Settings*

| LVDS_CNV_CLK_CNT | Clock Count Number |                     |  |  |
|------------------|--------------------|---------------------|--|--|
| Settings         | Single Lane Mode   | Dual Lane Mode      |  |  |
| 0b0000           | 3                  | 3                   |  |  |
| 0b0001           | 4                  | 4                   |  |  |
| 0b0010           | 5                  | 1/5                 |  |  |
| 0b0011           | 6                  | 2                   |  |  |
| 0b0100           | 7                  | Selection not valid |  |  |
| 0b0101           | 1                  | Selection not valid |  |  |
| 0b0110           | 2                  | Selection not valid |  |  |

As a overview guide, Table 21 indicates the minimum required LVDS\_CNV\_CLK\_CNT settings for various conversion rates.

The maximum tMSB of 22.4ns, that is with the gain error correction enabled (see the [Gain Error Correction](https://ccms.web.analog.com/oxygen-webapp/app/Keyref%20tdi1697028251825) section), is used for all calculations in Table 21.

On power-up, the value of the gain error correction is 0x200, disabling the correction and allowing for a lower latency result. In this case, tMSB is 18 ns and a latency of 48.21 ns can be achieved. To aid alignment of this valid result data position with the digital host of the user, the ADC Data Interface Configuration A register (see the [ADC Data Interface Configuration A Register](#page-79-0) section, Address 0x15) contains access to the interface check feature enabled by setting the INTF\_CHK\_EN bit. When this bit is set, the ADC results are no longer output on the interface, and the output is replaced with a fixed pattern 20b1010 1100 0101 1101 0110 (0xA C5D6). This feature allows the user to align and test the data interface to their digital host. When the INTF\_CHK\_EN bit is unset, the normal conversion results are output to the LVDS interface immediately. This method is useful for alignment, particularly for self clock mode cases where unknown PCB propagation delays may be present between the AD4086 and its digital host controller. Note that this feature was specifically designed to help output LVDS data with the LVDS clock of the digital host by using static data, and the feature does not indicate if the LVDS\_CNV\_CLK\_CNT setting is used.

*Table 21. LVDS\_CNV\_CLK\_CNT Settings for Various Sample Rates (with gain correction applied)*

| Sample Rate (MSPS) | LVDS Lanes | fCLK (MHz) | tCLK (ns) | (tMSB/tCLK) + 1.5 | LVDS_CNV_CLK_CNT Setting |
|--------------------|------------|------------|-----------|-------------------|--------------------------|
| 40                 | 1          | 280        | 3.571     | 7.772             | 7                        |
| 35                 | 1          | 245        | 4.082     | 6.988             | 6                        |
| 30                 | 1          | 210        | 4.762     | 6.204             | 6                        |
| 25                 | 1          | 175        | 5.714     | 5.420             | 5                        |
| 20                 | 1          | 140        | 7.143     | 4.636             | 4                        |
| 15                 | 1          | 105        | 9.524     | 3.852             | 3                        |
| 40                 | 2          | 140        | 7.143     | 4.636             | 4                        |

#### **LVDS Data Transfer Latency**

Where the user is concerned in knowing the overall latency from when an individual ADC conversion is initiated to the time when the LSB has reached the host controller, it is important to consider the data transfer latency. The total latency observed is the sum of the ADC latency and the data transfer latency, in this case, the LVDS\_CNV\_CLK\_CNT is set to achieve minimum ADC latency. Additional clock cycles more than the minimum required incur additional LVDS clock cycles of latency to the overall latency, as is shown in [Figure 76.](#page-47-0)

The data transfer latency on the LVDS interface depends on the following parameters:

- ► LVDS clock period, tCLK
- ► Number of active LVDS lanes, NLANES
- ► Number of bits to be read, NBITS

Calculate the latency as follows:

Data Transfer Latency = 
$$\frac{N_{BITS}}{N_{LANES}} \times t_{CLK}$$

For applications that require extremely low latencies, note that as the data is transferred MSB to LSB in both single and dual lane modes, and that there is no requirement to fully read a result from the interface, the data transfer latency can be reduced for lower resolution results (that is, NBITS can be chosen to be smaller than the maximum 14 bits available).

**[analog.com](http://www.analog.com/en/index.html) Rev. 0 | 47 of 91**

### <span id="page-47-0"></span>**DIGITAL INTERFACE**

![](_page_47_Figure_2.jpeg)

*Figure 76. LVDS Data Transfer Latency*

### **LVDS Output Differential Drive**

The AD4086 supports selection of the LVDS output differential voltage from one of three predetermined differential amplitudes of ±185mV p-p, ±240mV p-p, and ±325mV p-p assuming a termination resistance of 100Ω across the differential pair. The output common-mode voltage of the LVDS drive is adjusted for each selection automatically to ensure that the peak output voltage remains within the IOVDD rail. The current default selection sets the differential amplitude at ±240mV p-p. The output differential voltage can be modified by writing to the LVDS\_VOD bits of the ADC Data Interface Configuration C register (see the [ADC Data](#page-80-0) [Interface Configuration C Register](#page-80-0) section, Address 0x17).

#### **Data Interface Test Functions**

Regardless of the selected output configuration, the AD4086 is equipped with self test functions that enable verification of the integrity of the data interface physical layer, including device pads, PCB interconnect, and the host interface connections. An interface check function is available setting a fixed, 14-bit data pattern mode to output. Selection of this test function is made by writing to the INTF\_CHK\_EN bit in the Data Interface Configuration A register (see the [ADC Data Interface Configuration A Register](#page-79-0) section, Address 0x15).

By enabling the built-in test function, access to conversion results is suspended; therefore, only use this function at either power-up or during an idle period when conversion results are not required for normal system function.

Refer to the [ADC Result Latency and LVDS Interface Alignment](#page-44-0) section for further information.

#### **SPI DATA INTERFACE**

#### **SPI Data Interface Configuration**

For applications that do not require the interface bandwidth of the LVDS interface, such as when using asynchronous capture into the result FIFO, the data interface can be reconfigured into a single or quad lane, SPI data interface. In this configuration, the AD4086 outputs data on either one or four CMOS data lanes simultaneously at serial clock rates up to 50MHz. The result data is shifted out serially on the falling edge of the interface clock (DCLK). In SPI configuration, the AD4086 results can be read at interface rates up to 200MHz when using four SPI lanes.

To select the SPI configuration, program the DATA\_INTF\_MODE bit of the Data Interface Configuration A register (see the [ADC](#page-79-0) [Data Interface Configuration A Register](#page-79-0) section, Address 0x15) with Binary Sequence 1'b1. Once configured for SPI mode, the AD4086 LVDS drivers are automatically disabled, including the echo clock output (DCO+ and DCO−), preventing contention between LVDS and CMOS functions. As a result, the LVDS\_SELF\_CLK\_MODE and LVDS\_VOD settings no longer affect the operation of the data interface and can be left at their power-on defaults or another convenient value. Because the driver is disabled, the DCO+ and DCO− output pins can be left disconnected in the hardware design as these pins are unused.

As detailed in Table 22, the following LVDS pins are reconfigured as CMOS input or outputs to realize the SPI data interface.

*Table 22. LVDS/SPI Data Interface Pins Crossreference*

| LVDS Pin | CMOS Pin | Function                         |  |  |  |  |
|----------|----------|----------------------------------|--|--|--|--|
| CLK+     | DCLK     | Data interface clock input       |  |  |  |  |
| CLK−     | DCS      | Data interface chip select input |  |  |  |  |
| DA+      | SDOA     | Serial Data Output A             |  |  |  |  |
| DA−      | SDOB     | Serial Data Output B             |  |  |  |  |
| DB+      | SDOC     | Serial Data Output C             |  |  |  |  |
| DB−      | SDOD     | Serial Data Output D             |  |  |  |  |

As with LVDS configuration mode, SPI configuration selection allows control of the number of active lanes. For SPI data interface configuration, the user has the option to configure single lane SPI or quad lane SPI.

#### **SPI Active Data Lane Count**

The SPI can be configured to output the result data on either one or four data lanes, which is controlled by the SPI\_LVDS\_LANES bit in the ADC Interface Configuration A register (see the [ADC](#page-79-0) [Data Interface Configuration A Register](#page-79-0) section, Address 0x15). By default, this bit is set to 0 (one lane active), and can be set to 1 to use four data lanes. Note that this bit also sets the number of active data lanes for the LVDS interface. The data order and pin assignment to the serial data output (SDOx) pins is detailed in [Table 23](#page-48-0), and shown in [Figure 83.](#page-55-0)

**[analog.com](http://www.analog.com/en/index.html) Rev. 0 | 48 of 91**

### <span id="page-48-0"></span>**DIGITAL INTERFACE**

*Table 23. SPI Data Lane(s) Data Order and Pin Assignment*

|                        | Output Data Order                           |                                               |  |  |  |  |
|------------------------|---------------------------------------------|-----------------------------------------------|--|--|--|--|
| Serial Data Output Pin | One Active SPI Lane<br>(SPI_LVDS_LANES = 0) | Four Active SPI Lanes<br>(SPI_LVDS_LANES = 1) |  |  |  |  |
| SDOA                   | Not applicable                              | SDO 3                                         |  |  |  |  |
| SDOB                   | SDO 0                                       | SDO 2                                         |  |  |  |  |
| SDOC                   | Not applicable                              | SDO 1                                         |  |  |  |  |
| SDOD                   | Not applicable                              | SDO 0                                         |  |  |  |  |

# **Data Interface CRC**

To ensure the integrity of the result data, a CRC is appended to the FIFO results. This CRC is always enabled and appended. The computation of the result checksum is independent of that of the configuration interface. The result is 24 bits in length and is appended to each data result record acquired from the FIFO.

#### **Sign Extension**

When accessing the FIFO data with the SPI data interface, the 14-bit resolution of the AD4086 is not a convenient length for interfacing with microcontroller or microprocessor hosts. To make data access and storage simpler, the ADC result is sign extended to 24 bits. In this way, the data format aligns better with their selected host.

**GPIO PINS**

The AD4086 GPIO pins are intended to simplify the development of synchronous data acquisition applications by facilitating a simplified state control interface between the host processor, the data converter, and other related signal chain components. When configured as an output, these GPIO pins can be assigned as an indicator of device status, a digital control for a related signal chain component, or a serial data lane for device configuration. In input mode, the GPIO pins allow pin programming of converter features such as digital filter synchronization (reset) and an external event trigger.

The desired function for each GPIO is defined by writing to the GPIO Configuration A through GPIO Configuration C registers (Address 0x19 through Address 0x1B), see the [GPIO Configuration](#page-82-0) [A Register](#page-82-0) section through the [GPIO Configuration C Register](#page-84-0) section. The configuration for each GPIO includes an output enable bit, an output data bit, and a function selection. The output data bit determines the logical state of the output when the GPO data option is selected; otherwise, the output state is determined by the selected function, assuming the output is enabled. By default, GPIO0 is enabled as an output, and the configuration SPI SDO function is selected. All other GPIO outputs are disabled.

[Table 25](#page-49-0) provides a brief description of the available AD4086 GPIO functions. Each of the GPIO pins can be configured for any of the following functions.

*Table 24. GPIO Registers Overview*

| Register      | Bits                                                        | Contents                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
|---------------|-------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| GPIO_CONFIG_A | GPIO_0_EN,<br>GPIO_1_EN,<br>GPIO_2_EN,<br>GPIO_3_EN         | Enable bits for each GPIO.<br>0: Configures the GPIO as an input.<br>1: Configures the GPIO as an output.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| GPIO_CONFIG_A | GPIO_0_DATA,<br>GPIO_1_DATA,<br>GPIO_2_DATA,<br>GPIO_3_DATA | The corresponding GPIO_x_SEL bit for each GPIO can be set to 0111b to read or write data to that GPIO.<br>In this mode, GPIO_x_EN selects whether each of these data bits is read only or write only, depending on whether the GPIO is<br>configured as an input or an output.<br>When configured as an output, these bits are write only, the user can set the bits to a logic level that they need to output on the<br>GPIO.<br>When configured as an input, these bits are read only, the user can read the bits to determine the logic level input to on the GPIO.<br>If the corresponding GPIO_x_SEL is not set to 0111b, the GPIO_x_DATA is not valid as the GPIO is overridden with the selected<br>GPIO function. |
| GPIO_CONFIG_B | GPIO_0_SEL,<br>GPIO_1_SEL                                   | Selection for the function mode of GPIO0 and GPIO1.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| GPIO_CONFIG_C | GPIO_2_SEL,<br>GPIO_3_SEL                                   | Selection for the function mode of GPIO2 and GPIO3.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |

**[analog.com](http://www.analog.com/en/index.html) Rev. 0 | 49 of 91**

# <span id="page-49-0"></span>**DIGITAL INTERFACE**

#### *Table 25. GPIO\_x\_SEL Function Descriptions*

| GPIO_x_SEL | Function                 | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
|------------|--------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0000b      | Configuration SPI<br>SDO | Configuration Serial Data Output. This configures the selected GPIO to be the SDO for the configuration SPI.                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| 0001b      | FIFO full                | FIFO Memory Full Indication Output. This configures the selected GPIO to function as a FIFO full indicator. The FIFO full indicator<br>is set when the conversion result corresponding to the specified count in the FIFO watermark registers (see the FIFO Watermark<br>Register section, Address 0x1D and Address 0x1E) is loaded into the data FIFO. The FIFO full status bit is cleared by reading data<br>from the FIFO, and it is cleared when the first conversion result is moved from the FIFO to the data interface output shift register. |
| 0010b      | FIFO read done           | FIFO Memory Read Completed Output. This configures the selected GPIO to function as a FIFO read done indicator. The FIFO read<br>done indicator is cleared by default when the FIFO is first enabled, and each time the last conversion result is moved from the FIFO<br>into the data interface output shift register. The FIFO read done is cleared when the MSB of the last FIFO result is read on the selected<br>data interface.                                                                                                                |
| 0011b      | Filter result ready      | Filter Result Ready Output. When the digital filter is enabled, this configures the selected GPIO to function as an indicator that new<br>data is available to read on the interface. This active low indication allows synchronization between the host and the AD4086 when<br>utilizing the integrated digital filter to oversample and decimate an incoming signal. The signal is driven low at the end of each filter<br>decimation period and is driven high again before the next decimated output is ready.                                   |
| 0100b      | HI_DTCT                  | High Threshold Event Output. With threshold detection enabled, this configures the selected GPIO to indicate when the high level<br>threshold is crossed. The output is active high.                                                                                                                                                                                                                                                                                                                                                                 |
| 0101b      | LO_DTCT                  | Low Threshold Output. With threshold detection enabled, this configures the selected GPIO to indicate when the low level threshold is<br>crossed. The output is active high.                                                                                                                                                                                                                                                                                                                                                                         |
| 0110b      | ALERT                    | Status Alert (Active Low) Output. This configures the selected GPIO to function as the status alert for threshold event detection.                                                                                                                                                                                                                                                                                                                                                                                                                   |
| 0111b      | GPIO data                | General-Purpose Output Mode. In this mode, the state of the corresponding GPIO_x_DATA bit in the GPIO Configuration A register<br>(see the GPIO Configuration A Register section, Address 0x19) is applied to the configured output.                                                                                                                                                                                                                                                                                                                 |
| 1000b      | FILTER_SYNC              | Filter Synchronization Input (Active Low). This configures the selected GPIO to function as a synchronization signal for the digital filter.<br>When held low, this input holds the digital filter in reset.                                                                                                                                                                                                                                                                                                                                         |
| 1001b      | EXT_EVENT                | External Event Trigger Input. Event triggers when a logic high is detected on the configured GPIO input. This event can be used to<br>trigger the FIFO.                                                                                                                                                                                                                                                                                                                                                                                              |

**[analog.com](http://www.analog.com/en/index.html) Rev. 0 | 50 of 91**

# <span id="page-50-0"></span>**DIGITAL FEATURES**

#### **OVERVIEW**

The AD4086 includes several useful digital features that offer great solution benefits to many applications. These features can be individually enabled by the user, when required. A brief overview follows for these features, in depth explanation and definition of these features are found in the following sections.

- ► Event Detection: This feature allows the detection when the analog input has crossed user-configured thresholds. Such detections can be flagged in the configuration registers, output to a GPIO, or used to trigger the result FIFO.
- ► [Result FIFO](#page-52-0): This feature allows the acquisition of records of up to 16,384 conversion results into the on-chip memory. These acquisitions can be read back to the host controller via LVDS or the SPI data interface. The results stored in the FIFO can be either unprocessed ADC results or those that have been processed through the digital filter feature.
- ► [Digital Filter](#page-59-0): This feature offers three different digital filter configurations, each with a wide range of decimation rates, allowing oversampling benefits and the close control of the signal bandwidth.
- ► [System Error Correction Coefficients:](#page-66-0) Although the AD4086 offers excellent factory calibrated precision with minimal offset and gain errors, this feature allows the user to correct for signal chain that may be present within their application.

#### **EVENT DETECTION**

The AD4086 includes an event detection feature, whereby the user can either indicate when a particular analog input threshold level

is crossed or monitor a GPIO configured as an input. An internally generated event can then be used to set a flag in the configuration memory or routed to a configured GPIO output to be used to alert a host controller that a threshold condition is breached. It is also possible for a user to route an external signal to the AD4086 to be used as an external trigger. An internally or externally generated event can also be used to trigger the integrated result FIFO (see the [Result FIFO](#page-52-0) section). The mechanism for this is explained in the [Event Detection for FIFO](#page-52-0) section. The threshold detection compares a converted voltage code to a user-configured code because this is done in a sample by sample basis, and events immediately trigger, level hysteresis setting is also configurable to prevent unwanted triggering.

![](_page_50_Figure_11.jpeg)

*Figure 77. Internally Generated Event Detection Signal Path*

The Figure 77 serves as an aid with detailing the configuration and operation of the event detection of the AD4086.

| INT_EVENT_EN Bit |                |                                                           |                                                                                                                                                                                                                        |
|------------------|----------------|-----------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| (Address 0x1C)   | Mode           | Trigger Source                                            | Comment                                                                                                                                                                                                                |
| 0                | External event | GPIO_x_SEL = 4b1001, that is, configured for<br>EXT_EVENT | Event triggers when a logic high is detected on the<br>selected GPIO input.                                                                                                                                            |
| 1                | Internal event | ADC Results threshold detection is enabled.               | HI_THRESHOLD (Address 0x21 and Address 0x22) and<br>LO_THRESHOLD (Address 0x23 and Address 0x24) set<br>the upper and lower ADC result (or the digital filter result)<br>code threshold for the event to be triggered. |

**[analog.com](http://www.analog.com/en/index.html) Rev. 0 | 51 of 91**

# **DIGITAL FEATURES**

# **Event Detection Timing**

When event detection is enabled in the general configuration register (see the [General Configuration Register](#page-85-0) section), the HI\_DTCT and LO\_DTCT signals indicate the occurrence of an internally generated event. These signals can be routed internally through the following paths:

- ► HI\_DTCT and LO\_DTCT are directly accessible via an enabled GPIO with GPIO\_x\_SEL set to 0b100 or 0b101, respectively, a threshold event can be monitored externally by a digital host via the GPIO. Logic 1 on a configured GPIO indicates detection of an event.
- ► HI\_DTCT and LO\_DTCT can each be routed by setting the HI\_ROUTE and LO\_ROUTE bits to 1, respectively, in the general configuration register (Address 0x1C) to allow HI\_DTCT and LO\_DTCT to propagate to the LO\_STATUS and HI\_STATUS bits in the device status register (see the [Device Status Register](#page-78-0) section, Address 0x14). These status bits can be monitored by the digital host via the configuration SPI. Logic 1 on a configured GPIO indicates the detection of an event. Each of these two bits are independently cleared when a 1 is written to these bits. Power cycling or device reset also result in the bits clearing.
- ► HI\_DTCT and LO\_DTCT can each be routed by setting the HI\_ROUTE and LO\_ROUTE bits to 1, respectively, in the general

configuration register (Address 0x1C) to allow HI\_DTCT and LO\_DTCT to propagate to the ALERT signal. Any enabled GPIO set to output a status alert, that is, with GPIO\_x\_SEL set to 0b0110, routes the ALERT signal to the GPIO to indicate when an event occurs. A GPIO configured in this mode is normally high, with a logic low indicating that an event has occurred. As indicated in the [Figure 79](#page-52-0) section, this GPIO remains low only while the threshold level is crossed, and it returns to logic high as soon as the threshold bound is no longer crossed, and the timing in Figure 78 is satisfied.

Event detection is synchronous to the rising edge of the CNV+. A latency of two conversion clock cycles exists from the first CNV+ edge where the analog input crosses a threshold to a detected event that is flagged in the device status register and to any GPIO configured to route ALERT. As is evident in [Figure 77,](#page-50-0) where both the HI\_DTCT flag and ALERT routed to a GPIO are shown, the behavior, once the threshold level is no longer crossed, is different. When a CNV+ rising edge occurs where the analog input no longer crosses the set threshold, ALERT de-asserts two conversion cycles later, on the rising edge of CNV. Any HI\_DTCT or LO\_DTCT already set is not cleared at this point. These signals are only cleared by writing 1 to the relevant bits in the device status register (Address 0x14) or where a device reset occurred.

![](_page_51_Figure_9.jpeg)

*Figure 78. Event Detection Timing*

**[analog.com](http://www.analog.com/en/index.html) Rev. 0 | 52 of 91**

#### <span id="page-52-0"></span>**DIGITAL FEATURES**

#### **Threshold Detect Levels**

The threshold detection of the AD4086 includes a hysteresis setting. By configuring this setting, the user can ensure that unwanted threshold triggering can be avoided. Figure 79 shows how this can be achieved. A single hysteresis setting is configured, that is then applied to both the HI\_THRESHOLD and LO\_THRESHOLD bits. The high and low detection flags remain set until the hysteresis thresholds are crossed.

![](_page_52_Figure_4.jpeg)

*Figure 79. Threshold Detect Levels*

### **Enabling Event Detection**

By default, after power on or reset, HI\_ROUTE and LO\_ROUTE are set to Logic 0, masking the threshold level detection from generating any event alert. When enabled, the gated versions of these signals, HI\_DTCT\_GATED and LO\_DTCT\_GATED, are logic NOR'd to generate the ALERT signal. If a user requires the use of the HI\_DTCT, LO\_DTCT, or ALERT signals to flag an event occurrence externally, back to a digital host, the GPIO\_x\_SEL registers can be used to route any, or multiple, of these signals to the GPIO pins.

#### **Event Detection for FIFO**

Event detection can also be used to arm the on-chip FIFO. The event detection for the FIFO can be triggered using either internal or external events as detailed in the [Table 26](#page-50-0) section.

To use the ALERT signal to trigger the FIFO, the HI\_ROUTE and/or the LO\_ROUTE bits must be configured as required, and the INT\_EVENT\_EN bit must be set to 1, to use a combined ALERT output to trigger the FIFO. Alternately, when configured with the INT\_EVENT\_EN bit set to 0, a GPIO EXT\_EVENT input must be configured, and this input triggers the FIFO when a Logic 1 is presented on the GPIO. Because this event was generated externally, there is no ALERT signal generated.

The HI\_THRESHOLD (Address 021 and Address 022) and LO\_THRESHOLD (Address 0x23 and Address 0x 24) bits can be used to configure the ADC output code thresholds for the internal event detection. These bits can each be masked using the HI\_ROUTE and LO\_ROUTE bits in the general configuration register (Address 0x1C). Setting these bits logic high, routes the bits to be used for the ALERT flag (that can be monitored using a preconfigured GPIO), it is also enabled as a FIFO event trigger as well as making these available as HI\_STATUS and LO\_STATUS flags in the device status register (Address 0x14).

![](_page_52_Figure_13.jpeg)

*Figure 80. FIFO Event Detection Logic*

# **Event Detection ADC Data Result**

The ADC data result, as shown in [Figure 77](#page-50-0), is dependent of the selected data path. As is evident in [Figure 91,](#page-59-0) where the digital filter (see the [Digital Filter](#page-59-0) section) is enabled, the output of the selected filter refers to the ADC data result that is checked by the threshold detection for event detection.

### **RESULT FIFO**

A single port data FIFO was integrated into the AD4086 for applications where a reduced data interface transmission load is required and where asynchronous data capture and access is appropriate. This FIFO can serve to reduce the requirements for the digital host controller and can, for example, enable the AD4086 to be deployed in systems using an MCU digital host. The data FIFO allows for a record of up to 16,384 data results to be captured per acquisition burst without result loss due to data overflow. As a single port memory, simultaneous data interface read and ADC conversion result write operations are not permitted to the FIFO.

To allow synchronization of FIFO access between the host controller and ADC, status flags are included to indicate if the memory is full (FIFO\_FULL) or if no new data available in the FIFO (FIFO\_READ\_DONE), that is, there is no new data since the last trigger was set, or the last FIFO data read back of a result record has already been completed. When N = WATERMARK is reached, that is, when the conversion result corresponding to the specified count in the FIFO\_WATERMARK register is loaded into the data FIFO, memory is set as full, and the FIFO\_FULL bit gets asserted in device status register (see the [Device Status Register](#page-78-0) section, Address 0x4). The status bits can be accessed by reading directly from the device status register (Address 0x14) via the configuration SPI, appending the status to the data SPI frame, or by assigning the desired status flags to a GPIO pin by setting the required GPIO\_x\_SEL bit. Further details on these GPIO can be found in the [GPIO Pins](#page-48-0) section. The user can also select between various modes of initiating the burst acquisition, which will be described further in the [FIFO Mode Selection and Configuration](#page-53-0) section.

**[analog.com](http://www.analog.com/en/index.html) Rev. 0 | 53 of 91**

#### <span id="page-53-0"></span>**DIGITAL FEATURES**

# **FIFO Mode Selection and Configuration**

There are four distinct modes in which the data FIFO of the AD4086 can be configured. The active mode is selected by setting the FIFO\_MODE bits in the general configuration register (see the [General Configuration Register](#page-85-0) section, Address 0x1C). By default,

the FIFO is disabled (FIFO\_MODE = 00). The modes are designed to fit the use case requirements of different applications. Table 27 provides details about each FIFO mode and their applicable use cases.

*Table 27. FIFO Configuration Modes (FIFO\_MODE)*

| FIFO_MODE Bit<br>Value | FIFO Mode                                       | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | Use Case                                                                                                                                                                                                                                                                                                                                                       |
|------------------------|-------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 00                     | FIFO disabled                                   | FIFO is not used. This value also resets and rearms the event<br>trigger.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  | Continuous convert mode, and FIFO is not in use.                                                                                                                                                                                                                                                                                                               |
| 01                     | Immediate trigger mode                          | In this mode, the data capture is initiated immediately after<br>receipt of the first valid converter result and continues until [N =<br>WATERMARK] results are loaded into the FIFO memory.<br>Upon read back from the FIFO, FIFO_READ_DONE indicates<br>when [N = WATERMARK] results are read from the FIFO.                                                                                                                                                                                                                                                                                                             | User is interested in burst acquisition(s) of [N<br>= WATERMARK] results, initiated by setting this<br>FIFO_MODE, Bits[1:0] value.                                                                                                                                                                                                                             |
| 10                     | Event trigger capture, read<br>latest WATERMARK | The data capture into the FIFO memory is initiated by the<br>user-selected event method. The result counter initiates by<br>the event, and data captures to the FIFO stop once [N =<br>WATERMARK] results are captured.                                                                                                                                                                                                                                                                                                                                                                                                    | User is interested in burst acquisition(s) of [N =<br>WATERMARK] results, initiated by an event. Only result<br>data after the event is of interest.                                                                                                                                                                                                           |
|                        |                                                 | Upon read back from the FIFO, FIFO_READ_DONE indicates<br>when [N = WATERMARK] results have been read from the<br>FIFO.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |                                                                                                                                                                                                                                                                                                                                                                |
| 11                     | Event trigger capture mode,<br>read all FIFO    | The data capture immediately initiates after the receipt of the<br>first valid converter result.<br>The FIFO continuously fills until an event is detected. If no<br>event is detected before the FIFO fills (that is, 16,384 results<br>are written to memory), the memory continues to fill with the<br>oldest results discarded on a first in, first out basis.                                                                                                                                                                                                                                                         | User is interested in burst acquisition(s) of [N =<br>WATERMARK] results initiated by an event. The full<br>FIFO contents are read in this mode. In this mode, the<br>user can read [N = WATERMARK] results after the event<br>and (16,384 − [N = WATERMARK]) before the event.<br>Only WATERMARK values that are multiples of four are<br>valid in this mode. |
|                        |                                                 | Upon receipt of the selected event method, a result counter<br>counts up to [N = WATERMARK]. Data capture stops once the<br>WATERMARK is reached. In this mode, once the FIFO is filled,<br>the position in the FIFO memory at which the event occurred<br>gets automatically stored in the FIFO_WATERMARK register.<br>The value read back from FIFO_WATERMARK allows the user<br>to distinguish which of the stored results captured before the<br>event from those that were captured after the event. Further<br>details can be seen in the example given in the Event Trigger<br>Capture Mode, Read All FIFO section. |                                                                                                                                                                                                                                                                                                                                                                |
|                        |                                                 | Upon read back from the FIFO, FIFO_READ_DONE indicates<br>when 16,384 results are read from the FIFO. The full memory<br>read back contains [N = WATERMARK] results after the event.<br>If N in this case is less than 16,384, the remaining contents of<br>the FIFO contain the conversion results prior to the event.                                                                                                                                                                                                                                                                                                    |                                                                                                                                                                                                                                                                                                                                                                |

**[analog.com](http://www.analog.com/en/index.html) Rev. 0 | 54 of 91**

# **DIGITAL FEATURES**

#### **FIFO Event Detection**

The FIFO is configured for capture in event detection mode (FIFO\_MODE = 10 or FIFO\_MODE = 11, the following event detection options (see the [Table 26](#page-50-0) section) are available.

The general configuration register (Address 0x1C) contains the internal event enable bit (INT\_EVENT\_EN) which determines whether the AD4086 FIFO is to respond to an external or internal event trigger. The default state of this bit on power on and reset is INT\_EVENT\_EN = 0, which is configured for an external event.

#### **Asynchronous Data Capture**

To use the FIFO for asynchronous capture, first write to the FIFO watermark register (see the [FIFO Watermark Register](#page-86-0) section, Address 0x1D) with the number of conversions to be captured in each burst; any integer between 1 and 16,384 can be entered. If using GPIO to pass the FIFO status bits to the host controller, program those selections into the GPIO configuration registers prior to initiating the capture. Refer to the [GPIO Pins](#page-48-0) sections for further detail on GPIO configuration.

The final steps in initiating an asynchronous capture into the data FIFO include enabling the FIFO and then starting the conversion

clock. To enable the data FIFO in the general configuration register (see the [General Configuration Register](#page-85-0) section, Address 0x1C), the FIFO\_MODE bits must be set to immediate trigger mode (01). In this mode, the FIFO stores the results of the most recent FIFO\_WATERMARK samples and then automatically disables capture into the memory. The results can then be accessed through the SPI data interface or LVDS interface.

When the FIFO is enabled, each conversion result is loaded into the internal memory on the rising edge of the convert start signal, CNV. Internal timing dictates that FIFO\_WATERMARK + three conversion clocks are required to write FIFO\_WATERMARK sample results into the FIFO memory. See [Figure 82](#page-55-0) and [Figure 83](#page-55-0) for additional information.

The Figure 81 timing diagram shows an example where FIFO\_WA-TERMARK is set to 1000, and the first ADC results after the event occurred is captured by the FIFO after the third CNV. After N = 1000, that is, it has reached the FIFO\_WATERMARK value, FIFO\_FULL is asserted, and data stops being captured into the FIFO.

![](_page_54_Figure_11.jpeg)

*Figure 81. FIFO Data Capture Example, WATERMARK = 1000*

**[analog.com](http://www.analog.com/en/index.html) Rev. 0 | 55 of 91**

#### <span id="page-55-0"></span>**DIGITAL FEATURES**

#### **Asynchronous Read Access**

Access to the FIFO data is made through either a LVDS configuration (single lane only) or the multi-output SPI configuration of the data interface after the capture has completed. As a result, access is asynchronous to the capture process, and there are no specific timing restrictions between the conversion and interface clocks. Synchronization between the data FIFO and the data interface clock domain requires each read access to begin with

a header followed by a transfer of M bytes of conversion data; where M equals the product of the total number of results specified in the FIFO\_WATERMARK register (Address 0x1D and Address 0x1E) and the integer length in bytes (for SPI data interface) of a single conversion result. Note that the number of active data lanes reduces the access period by a factor of 2 for each doubling of the number of active lanes.

![](_page_55_Figure_5.jpeg)

*Figure 82. Asynchronous Capture Read Timing, Data FIFO Enabled, Single Data Lane*

![](_page_55_Figure_7.jpeg)

*Figure 83. Asynchronous Capture Read Timing, Data FIFO Enabled, Quad Data Lane Configuration*

![](_page_55_Figure_9.jpeg)

*Figure 84. Asynchronous Capture Read Timing, Data FIFO Enabled, LVDS Configuration*

**[analog.com](http://www.analog.com/en/index.html) Rev. 0 | 56 of 91**

#### **DIGITAL FEATURES**

# **FIFO Timing Considerations**

#### **Immediate Trigger Mode**

Figure 86 illustrates the timing relationship between the command to arm the FIFO for data write access and the point at which the FIFO is armed. Figure 86 shows an example of where single lane SPI data access is configured and FIFO\_FULL and FIFO\_READ\_DONE are output to GPIO. Because a capture has not yet been initiated, FIFO\_FULL and FIFO\_READ\_DONE are driven low. A free running CNV clock is shown in this example. Upon receipt of the update to the general configuration register (Address 0x1C), the FIFO controller advances to an idle state

on the next rising edge of CNV. The FIFO then advances to the writing state after two further CNV clock edges and begins filling the FIFO until WATERMARK results are loaded and FIFO\_FULL is generated.

Upon completion of reading the FIFO data, a rearming event for immediate mode capture involves disabling the FIFO by writing 00 to FIFO\_MODE then re-enabling by writing 01 to the FIFO mode to arm the FIFO for a new capture. As is the case with the initial arming, the FIFO advances to the idle state upon receipt of the first rising edge of CNV after the configure instruction to arm the FIFO is issued. The sequence and timing is the same as for the initial FIFO arming. See Figure 86.

![](_page_56_Figure_7.jpeg)

*Figure 85. Immediate Trigger Mode Arming*

![](_page_56_Figure_9.jpeg)

*Figure 86. Immediate Trigger Mode Rearming*

**[analog.com](http://www.analog.com/en/index.html) Rev. 0 | 57 of 91**

# **DIGITAL FEATURES**

# **Event Triggered Capture, Read Latest WATERMARK**

Event triggered (read latest) mode is used where there is interest only in the ADC data after an event occurs. This event can be an internally generated event, where the AD4086 is running continuously, and the threshold detection is enabled to trigger an event as soon as an ADC input threshold is crossed. Or, the user can be independently monitoring the system or ADC input for an event, and an external event trigger is user-issued via a configured GPIO. As in all cases of arming the FIFO, the first rising edge after a FIFO\_MODE write command arms the FIFO for data capture; however, no data is written to the FIFO until an event of the selected method occurs.

Rearming the trigger involves a similar process to the immediate mode rearming. The FIFO is firstly disabled by writing 00 to the FIFO\_MODE bits before, and then rearmed by again enabling the required capture mode.

![](_page_57_Figure_6.jpeg)

*Figure 87. Event Triggered Capture, Read Latest WATERMARK Arming*

**[analog.com](http://www.analog.com/en/index.html) Rev. 0 | 58 of 91**

# <span id="page-58-0"></span>**DIGITAL FEATURES**

#### **Event Trigger Capture Mode, Read All FIFO**

Event triggered mode can be used where ADC results immediately prior to the event, as well as those after, are of interest to the user. Once armed, the FIFO continuously fills with new ADC results, storing up to, at most, 16,384 of the most recent results, wrapping around and overwriting the oldest results in FIFO memory once 16,384 captures are made.

Once a trigger event occurs, the FIFO continues to capture WA-TERMARK number of results after the event. Only multiples of four are valid values to set the FIFO\_WATERMARK register when using this mode. After an event has occurred, and the WATERMARK number of results has been captured in the FIFO, no further new results are captured until the FIFO is rearmed. The user must read back all 16,384 FIFO results, and the value set for FIFO\_WATER-MARK allows the user to determine where in the FIFO result data that the event occurred and also to distinguish between results that occurred before the event and those which occurred after the event as shown in Figure 89 and Figure 88. In the full FIFO read back, the first result after the event triggered is located at 16384 − (FIFO\_WATERMARK − 1), where FIFO\_WATERMARK is the value set prior to arming the capture. If this capture mode is armed and an event occurs before the FIFO wraps around once, the FIFO results before the event contain either results from previous FIFO use or, when used for the first time after power cycling the device, the FIFO contains random data in the FIFO data locations before the event.

*Figure 88. Event Capture Mode Read All FIFO Mode Example, FIFO Filling*

![](_page_58_Picture_7.jpeg)

*Figure 89. FIFO Event Capture Mode Read All FIFO Mode Example, Locating Event Position in FIFO*

![](_page_58_Figure_9.jpeg)

*Figure 90. Event Trigger Capture Mode, Read All FIFO Rearming*

**[analog.com](http://www.analog.com/en/index.html) Rev. 0 | 59 of 91**

# <span id="page-59-0"></span>**DIGITAL FEATURES**

#### **DIGITAL FILTER**

The AD4086 includes the option of enabling an integrated digital filter for applications where noise rejection by bandwidth limiting is desired. As shown in Figure 91 and detailed as follows, there are four paths available by which to route digital data: no digital filtering, a sinc1 filter, a sinc5 filter, or a sinc5 compensated filter.

Further details on each of these filters is described in the following sections. To ensure the first filter result produces the correct data, when a user makes a change to the filter selection, a reset must be issued via the GPIO pin configured for filter synchronization (FILTER\_SYNC).

![](_page_59_Figure_5.jpeg)

*Figure 91. Digital Filter Selection Options*

#### **Benefits of Digital Filtering**

The ADC result path can be configured to use the integrated digital filter feature. The filter configuration register (see the [Filter Configu](#page-89-0)[ration Register](#page-89-0) section, Address 0x29) contains the FILTER\_SEL bits that allow the user to bypass (default register setting) the digital filter or select from one of three filter options. Each filter has unique bandwidth profile properties that allows high flexibility in allowing selection to be made depending on the end application requirements. Table 28 shows the −3dB bandwidths achievable for each user-selectable filter type. The SINC\_DEC\_RATE bits controls the bandwidth and the data decimation factor.

These filters allow the user to programmatically control the noise bandwidth of their signal chain and also can offer benefits by reducing the amount filtering required in the analog front end, while offering dynamic range improvement without the need for additional components. The digital filter response sections have addition details on the different filter profiles that include the following:

- ► Sinc1 has a wider bandwidth but is not optimized for pass-band flatness.
- ► Sinc5 has a flatter pass-band response; however, with a reduced bandwidth.
- ► Sinc5 + compensation is a filter highly optimized to give excellent pass-band flatness with a ripple within ±0.1dB.

*Table 28. Filter Bandwidth*

| Filter Type          | SINC_DEC_RATE | Decimation | −3 dB Bandwidth |  |
|----------------------|---------------|------------|-----------------|--|
| Sinc1                | 0000          | 2          | 0.25 × fS       |  |
| Sinc1                | 0001          | 4          | 0.114 × fS      |  |
| Sinc1                | 0010          | 8          | 0.056 × fS      |  |
| Sinc1                | 0011          | 16         | 0.028 × fS      |  |
| Sinc1                | 0100          | 32         | 0.014 × fS      |  |
| Sinc1                | 0101          | 64         | 0.007 × fS      |  |
| Sinc1                | 0110          | 128        | 0.0035 × fS     |  |
| Sinc1                | 0111          | 256        | 0.0017 × fs     |  |
| Sinc1                | 1000          | 512        | 0.0009 × fS     |  |
| Sinc1                | 1001          | 1024       | 0.0004 × fS     |  |
| Sinc5                | 0000          | 2          | 0.117 × fS      |  |
| Sinc5                | 0001          | 4          | 0.0525 × fS     |  |
| Sinc5                | 0010          | 8          | 0.0256 × fS     |  |
| Sinc5                | 0011          | 16         | 0.0127 × fS     |  |
| Sinc5                | 0100          | 32         | 0.0064 × fS     |  |
| Sinc5                | 0101          | 64         | 0.0032 × fS     |  |
| Sinc5                | 0110          | 128        | 0.0016 × fS     |  |
| Sinc5                | 0111          | 256        | 0.0008 × fS     |  |
| Sinc5 + Compensation | 0000          | 4          | 0.1015 × fS     |  |
| Sinc5 + Compensation | 0001          | 8          | 0.0506 × fS     |  |
| Sinc5 + Compensation | 0010          | 16         | 0.0253 × fS     |  |
| Sinc5 + Compensation | 0011          | 32         | 0.0127 × fS     |  |

**[analog.com](http://www.analog.com/en/index.html) Rev. 0 | 60 of 91**

# **DIGITAL FEATURES**

#### *Table 28. Filter Bandwidth (Continued)*

| Filter Type          | SINC_DEC_RATE | Decimation | −3 dB Bandwidth |  |
|----------------------|---------------|------------|-----------------|--|
| Sinc5 + Compensation | 0100          | 64         | 0.0063 × fS     |  |
| Sinc5 + Compensation | 0101          | 128        | 0.0032 × fS     |  |
| Sinc5 + Compensation | 0110          | 256        | 0.0016 × fS     |  |
| Sinc5 + Compensation | 0111          | 512        | 0.0008 × fS     |  |

**[analog.com](http://www.analog.com/en/index.html) Rev. 0 | 61 of 91**

# <span id="page-61-0"></span>**DIGITAL FEATURES**

#### **Filter Decimation Configuration**

Configuration of the digital filter is done through the filter configuration register (see the [Filter Configuration Register](#page-89-0) section, Address 0x29). The FILTER\_SEL bits select the active filtering path (that is, what filters are active), with each path having different allowed decimation rates (see Table 29).

*Table 29. Digital Filters Decimation Options According to FILTER\_SEL Bits Value*

| FILTER_SEL<br>Bits Value | Active Filter               | Allowed Decimation Rates                    |
|--------------------------|-----------------------------|---------------------------------------------|
| 0b00                     | No filtering (default)      | No decimation                               |
| 0b01                     | SINC1 filter                | 2, 4, 8, 16, 32, 64, 128, 256,<br>512, 1024 |
| 0b10                     | SINC5 filter                | 2, 4, 8, 16, 32, 64, 128, 256               |
| 0b11                     | SINC5 + compensation filter | 4, 8, 16, 32, 64, 128, 256, 512             |

The decimation factor is set via the SINC\_DEC\_RATE bits in the filter configuration register (see [Table 62](#page-89-0) for the encoding).

The readiness of new filter data can be indicated to the host controller via a GPIO pin by setting one of GPIO\_x\_SEL bits in either GPIO Configuration B register (see the [GPIO Configuration B](#page-83-0) [Register](#page-83-0) section, Address 0x1A) or GPIO Configuration C register (see the [GPIO Configuration C Register](#page-84-0) section, Address 0x1B) to 0011 (filter result ready (active low)). Until new data is available to the interface, the data from the previous result remains in the output shift register. The user must ensure that the same LVDS clock rate is maintained, and the user can either reread or disregard the repeated result data, which is shown in Figure 92, where a decimate by 4 example is used.

![](_page_61_Figure_8.jpeg)

*Figure 92. Digital Filter Decimate by 4 Frame Overview*

**[analog.com](http://www.analog.com/en/index.html) Rev. 0 | 62 of 91**

# **DIGITAL FEATURES**

# **Filter Reset Conditions**

### **Direct LVDS**

When accessing the filtered data directly via the LVDS interface, the AD4086 resets the filter by the following two methods:

- ► By configuring the filter, by issuing a write to the filter configuration register, Bits[7:0] (see the [Filter Configuration Register](#page-89-0) section, Address 0x29).
- ► By asserting a GPIO that' is configured for FILTER\_SYNC operation.

#### **With FIFO**

When the FIFO is enabled, the user must use a GPIO configured as FILTER\_SYNC to reset the filter for each FIFO acquisition.

### **Filter Synchronization**

Set GPIO\_x\_SEL to FILTER\_SYNC to configure this input providing synchronization to the controller of the user, which can be used to synchronize the filters across multiple AD4086 devices. The FILTER\_SYNC signal timing requirements for a filter reset are shown in Figure 93.

![](_page_62_Figure_11.jpeg)

*Figure 93. Filter Reset Timing*

**[analog.com](http://www.analog.com/en/index.html) Rev. 0 | 63 of 91**

# **DIGITAL FEATURES**

#### **Filter Result Ready Indicator**

Setting the GPIO\_x\_SEL bits to 0011 configures the GPIO to output the FILTER\_RESULT\_RDY signal, which is an active low logic signal that indicates to the host controller when each new filter result is complete. When LVDS is used to directly read out the filter results, this indicator can alert the user when each new filtered conversion result is available to read via the interface.

### **Filter Interface Timing Considerations**

Continuous access to filtered data results is available only through the LVDS data interface. SPI data interface access to filtered results is only made via the FIFO. The timing considerations, in this case, are described in the Filter Interface Timing Considerations when Using the FIFO section. For use with the LVDS data interface, it is recommended to use a GPIO, configured with the appropriate GPIO\_x\_SEL (0011) to output the filter result ready (active low) signal, as is shown in the example [Figure 92](#page-61-0) timing diagram.

# **Filter Interface Timing Considerations when Using the FIFO**

Figure 94 serves as an example to illustrate the sequence of events in this mode of operation. This example illustrates a sinc1 filter with

a decimate by 2 setting, where three results (that is, WATERMARK = 3) are configured to be stored in the FIFO. When using the integrated digital filters with the FIFO, the filter must be reset prior to each FIFO acquisition record. This reset must be given on the first CNV rising edge, where the FILTER\_SYNC signal must be brought low at least 15ns prior to the CNV edge and then released at least 5ns before the next rising edge. The first ADC result is ready tMSB after the second CNV rising edge. This first ADC result is latched into the filter on the third CNV rising edge. The fourth CNV rising edge latches the second ADC result into the digital filter. On the fifth rising edge, the first decimate by 2 result is complete, which is indicated by the FILTER\_READY signal going active on the fifth rising edge. This first filtered result is loaded into the FIFO on the sixth CNV rising edge. Because this example uses WATERMARK = 3, when three filtered (that is, six core ADC results, decimated by 2) results are loaded to the FIFO, the WATERMARK is reached, and FIFO\_FULL is asserted to indicate to the user that a FIFO record is available to read via the configured data interface (that is, the LVDS data lane(s) of the SPI data lane(s)). To initiate a subsequent FIFO record acquisition of the filtered ADC results, the user must start the whole sequence over, beginning again with the reset of the digital filter by bringing the FILTER\_SYNC signal low on the first rising edge of CNV.

![](_page_63_Figure_9.jpeg)

*Figure 94. Description of Filter Timing with FIFO*

**[analog.com](http://www.analog.com/en/index.html) Rev. 0 | 64 of 91**

#### **DIGITAL FEATURES**

#### **Digital Filter Conversion Pulses**

The total number of CNV pulses required for a single filter decimated result (sinc1 settling clocks) can be calculated using the following formula:

$$Settling \ CNV \ Pulses_{SINC1} = 2 + (D+1)$$

Note that each of the three filter types has a unique formula to determine the number of clocks required.

For the sinc5 settling clocks, the equation is as follows:

Settling CNV Pulses<sub>SINC5</sub> = 
$$2 + (5 \times D + 4)$$

For the sinc5 with compensation settling clocks, the equation is as follows:

Settling CNV Pulses<sub>SINC5 + COMP</sub> = 
$$2 + (35 \times D + 10)$$

where D equals the decimation rate (2, 4, 8 …).

#### **Sinc1 Settling Clocks**

Settling CNV PulsesSINC1 = 2 + D + 1

#### **Sinc5 Settling Clocks**

Settling CNV PulsesSINC5 = 2 + 5 × D + 4

#### **Sinc5 (with Compensation) Settling Clocks**

Settling CNV PulsesSINC5 + COMP = 2 + 35 × D + 10

#### **Digital Filtering Settling Time**

The settling time for the selected filter is the number of settling clocks times tCONV, as follows:

Filter Settling Time = (Settling CNV Pulses<sub>FILTERTYPE</sub>) 
$$\times$$
  $t_{CONV}$ 

#### **Digital Filtering Settling Time when Using FIFO**

When using the FIFO with filtered data, it is important to note that each new FIFO record of results must begin by issuing a FILTER\_SYNC signal on the first CNV to reset and initialize the filter and to prevent unflushed data from being contained in the first FIFO record result.

The minimum total number of conversion pulses required to fill a full FIFO record can be calculated as follows:

Total Required CNVs = D×WATERMARK + Settling CNV PulsesFILTERTYPE

where D equals the decimation rate (2, 4, 8 …).

# **Required Total Number of Conversion Pulses to Fill FIFO**

Total Required CNVs = D × WATERMARK + Settling CNV PulsesFILTERTYPE

#### **Digital Filter Response**

#### **Sinc1 Filter**

![](_page_64_Figure_29.jpeg)

*Figure 95. Sinc1 Filter Response, Decimate by 2*

![](_page_64_Figure_31.jpeg)

*Figure 96. Sinc1 Filter Response, Decimate by 4*

**[analog.com](http://www.analog.com/en/index.html) Rev. 0 | 65 of 91**

# **DIGITAL FEATURES**

![](_page_65_Figure_2.jpeg)

*Figure 97. Sinc1 Filter Response, Decimate by 8*

![](_page_65_Figure_4.jpeg)

*Figure 98. Sinc1 Filter Response, All Decimation Rates*

### **Sinc5 Filter**

![](_page_65_Figure_7.jpeg)

*Figure 99. Sinc5 Filter Response, All Decimation Rates*

#### **Filter Sinc5 + Compensation Filter**

![](_page_65_Figure_10.jpeg)

*Figure 100. Sinc5 + Compensation Filter Response, Decimate by 2*

![](_page_65_Figure_12.jpeg)

*Figure 101. Sinc5 + Compensation Filter Response, Decimate by 2, Pass-Band Ripple*

![](_page_65_Figure_14.jpeg)

*Figure 102. Sinc5 + Compensation Filter Response*

**[analog.com](http://www.analog.com/en/index.html) Rev. 0 | 66 of 91**

# <span id="page-66-0"></span>**DIGITAL FEATURES**

# **SYSTEM ERROR CORRECTION COEFFICIENTS**

Systematic gain and offset errors exist in all practical data acquisition circuits, and thus, the need for correction is essential to maximize the precision of the measurement channel. While these quantities can be corrected for in the host processor, implementation can be inefficient and consume more power than if integrated within the data converter. To minimize these challenges for the end user, the AD4086 has integrated both gain and offset correction on a per sample basis.

To describe the available error corrections, consider that the transfer function of an ideal ADC can be described by the straight line equation.

$$y = mx + c \tag{2}$$

This equation can be applied to the ADC transfer function where: *y* is the corrected ADC result. *m* is the gain or slope of the line. *x* is the uncorrected ADC result. *c* is the offset.

The gain or slop of the line can be described as follows:

$$m = (y2 - y1)/(x2 - x1)$$

where the following are in volts:

y2 is the input voltage at close to the positive full-scale input. y1 is the input voltage at close to the negative full-scale input. x2 is the converted voltage with the y2 voltage applied at the input. x1 is the converted voltage with the y1 voltage applied at the input.

The ideal slope or gain is m = 1V/V.

The system error correction coefficients in the Offset Error Correction and Gain Error Correction sections detail how signal chain errors in offset (c) and gain (m) can be corrected using the configuration registers of the AD4086.

# **Offset Error Correction**

The AD4086 is factory calibrated to give low zero error. To account for system offset errors that may be present in a users application signal chain, an offset error correction function was included, which allows users to correct for system offsets in their application by applying a code to the OFFSET bit field in the offset register at Address 0x24 and Address 0x25, Bits[11:0]. This bit field is a 12-bit value in a twos compliment data format.

The bit field is a 12-bit value in a twos compliment data format and OFFSET LSB represents the value of the ADC LSB as defined in the [Transfer Function](#page-18-0) section. The range of offset error correction is therefore defined as −2048 × LSB (0x800) to +2047 × LSB (0x7FF). This represents a voltage range of ±11.71mV for the specified VREFIN = 3.0V. The default value for this register, after power on, or after a software reset, is 0x000, which represents the zero offset correction applied.

# **Gain Error Correction**

The AD4086 is a high precision ADC with factory calibrated, gain error correction. To allow a user to correct for any signal chain gain error within their application, the GAIN register (see the [Gain](#page-88-0) [Correction Register](#page-88-0), Address 0x27 and Address 0x28) can be used. The GAIN bit field is a 10-bit value that allows a nominal gain error correction of ±1.5594% of full scale. The 10-bit register is coded in a straight binary data format, where the default value after power on, or software reset, is 0x200. This value represents no gain error correction being applied to the ADC results.

With the GAIN register first set to the default 0x200 value, the user can perform a two-point voltage measurement, preferably close to positive and negative full-scale inputs, and use the slope or gain equation in the System Error Correction Coefficients section to determine their system gain error. This system error can then be adjusted with a resolution of 1.5594%/512 = 0.00305%. The required correction calculated can be input to the GAIN register.

**[analog.com](http://www.analog.com/en/index.html) Rev. 0 | 67 of 91**

# <span id="page-67-0"></span>**LAYOUT GUIDELINES**

The AD4086 includes all critical bypass capacitors within the device package, which greatly reduces the layout challenge for a precision, high-speed converter. These integrated capacitors are optimally placed within the device package to ensure that maximum performance is easily obtained. However, as with any precision mixed signal device, care must be taken in system device placement to ensure that there is proper partitioning of the critical analog signal chain component routing and routing of the high-speed digital signals to prevent unwanted coupling effects.

Note the following layout considerations:

- ► The AD4086 contains internal decoupling on all power supplies, AVDD33 (0.47μF), VDD11 (1.88μF), IOVDD (0.22μF), as well as VDDLDO (0.22μF). Therefore, no external bypass capacitors are required, saving board space and reducing bill of material (BOM) count and sensitivity.
- ► Ensure good partitioning of analog and digital domain signals within the design by, for example, having all analog signals in

- from the left-hand side and keeping dynamic digital signals on the right-hand side.
- ► Have a solid ground plane under the AD4086 and connect all analog ground (GND) pins, reference ground (REFGND), and digital ground (IOGND) pins to this shared plane.
- ► Recommended connections of ground (GND), reference ground (REFGND), and digital ground (IOGND) connections are shown in Figure 103. It is recommended to not keep the current return path of the reference IC in the same current loop as the current return loop from the other circuitry on the PCB. Connect the reference local star point to the ADC star point ground on the top layer of the PCB as shown in Figure 103.
- ► See Figure 104 for the side view cross-section of the PCB board showing the ground planes distribution . Note that Figure 104 only shows the ground planes but does not including the signal tracks.

![](_page_67_Figure_10.jpeg)

*Figure 103. AD4086 External Reference Ground Connections*

![](_page_67_Figure_12.jpeg)

*Figure 104. Recommended PCB Ground Planes Layout*

**[analog.com](http://www.analog.com/en/index.html) Rev. 0 | 68 of 91**

# <span id="page-68-0"></span>**CONFIGURATION REGISTERS**

The features of the AD4086 family have been designed to simplify the application of low latency data capture to a broad array of measurement applications. This simplification is achieved through customization of the data interface, data path, and data access method to satisfy both measurement and the host processor interface requirements via the available configuration registers.

The register space was organized in contiguous regions by function to streamline device configuration as described in Table 30. As a result, the interface streaming functions (see the [Instruction Mode](#page-35-0) [Selection](#page-35-0) section) can be leveraged to simplify device configuration to a single SPI frame consisting of an instruction word and associated data. For most applications, modifications to the register space address range of Address 0x15 to Address 0x29 are sufficient. Modification of content in the configuration interface and product ID space (Address 0x00 to Address 0x11) is only necessary to initiate a software reset or to change the configuration access method. Note that changes to the configuration access method are outside the scope of this document. For assistance with these options, contact your [local Analog Devices sales representative](https://www.analog.com/en/support/find-sale-office-distributor.html) or submit a request for technical assistance through the Precision ADCs page on the [ADI Engineer Zone](https://ez.analog.com/data_converters/precision_adcs/).

*Table 30. Register Map Organization*

| Address Range                                          | Function                     |  |  |  |
|--------------------------------------------------------|------------------------------|--|--|--|
| 0x00 to 0x11<br>Configuration interface and Product ID |                              |  |  |  |
| 0x14                                                   | Device status                |  |  |  |
| 0x15 to 0x17                                           | Interface configuration      |  |  |  |
| 0x18 to 0x1B                                           | Power and GPIO configuration |  |  |  |
| 0x1C                                                   | General configuration        |  |  |  |
| 0x1C to 0x1E                                           | FIFO configuration           |  |  |  |
| 0x1F to 0x24                                           | Internal event detection     |  |  |  |
| 0x25 to 0x28                                           | System error correction      |  |  |  |
| 0x29                                                   | Digital filter configuration |  |  |  |

*Table 31. Configuration Register Summary—Configuration Interface Functions (Address 0x00 to Address 0x11)*

|      | Addr Name              | Bits  | Bit 7           | Bit 6                       | Bit 5                | Bit 4           | Bit 3                     | Bit 2                     | Bit 1       | Bit 0 | Reset | R/W |
|------|------------------------|-------|-----------------|-----------------------------|----------------------|-----------------|---------------------------|---------------------------|-------------|-------|-------|-----|
| 0x00 | INTERFACE_<br>CONFIG_A | [7:0] | SW_<br>RESET    | RE<br>SERVED                | ADDR_<br>ASCENSION   | SDO_<br>ENABLE  |                           | RESERVED<br>SW_<br>RESETX |             |       | 0x10  | R/W |
| 0x01 | INTERFACE_<br>CONFIG_B | [7:0] | SINGLE_<br>INST |                             | RESERVED             |                 | SHORT_<br>INSTRUC<br>TION | RESERVED                  |             |       | 0x00  | R/W |
| 0x02 | DEVICE_<br>CONFIG      | [7:0] |                 | RESERVED<br>OPERATING_MODES |                      |                 |                           |                           |             | 0x00  | R/W   |     |
| 0x03 | CHIP_TYPE              | [7:0] |                 | RESERVED<br>CHIP_TYPE       |                      |                 |                           |                           |             | 0x07  | R     |     |
| 0x04 | PRODUCT_<br>ID_L       | [7:0] |                 | PRODUCT_ID[7:0]             |                      |                 |                           |                           |             | 0x56  | R     |     |
| 0x05 | PRODUCT_<br>ID_H       | [7:0] |                 | PRODUCT_ID[15:8]            |                      |                 |                           |                           | 0x00        | R     |       |     |
| 0x06 | CHIP_GRADE             | [7:0] |                 | GRADE<br>DEVICE_REVISION    |                      |                 |                           |                           |             |       | 0x02  | R   |
|      | 0x0A SCRATCH_<br>PAD   | [7:0] |                 |                             |                      |                 | SCRATCH_VALUE             |                           |             |       | 0x00  | R/W |
|      | 0x0B SPI_<br>REVISION  | [7:0] |                 | SPI_TYPE                    |                      |                 |                           | VERSION                   |             |       | 0x83  | R   |
|      | 0x0C VENDOR_L          | [7:0] |                 |                             |                      |                 | VID[7:0]                  |                           |             |       | 0x56  | R   |
|      | 0x0D VENDOR_H          | [7:0] |                 |                             |                      |                 | VID[15:8]                 |                           |             |       | 0x04  | R   |
|      | 0x0E STREAM_<br>MODE   | [7:0] |                 |                             |                      |                 | LOOP_COUNT                |                           |             |       | 0x00  | R/W |
| 0x0F | TRANSFER_<br>CONFIG    | [7:0] |                 |                             | RESERVED<br>KEEP_    |                 |                           | STREAM_<br>LENGTH_VAL     | RESERVED    |       | 0x00  | R/W |
| 0x10 | INTERFACE_<br>CONFIG_C | [7:0] |                 | CRC_ENABLE                  | STRICT_<br>REGISTER_ | SEND_<br>STATUS |                           | ACTIVE_INTERFACE_MODE     | CRC_ENABLEB |       | 0x23  | R/W |

**[analog.com](http://www.analog.com/en/index.html) Rev. 0 | 69 of 91**

# **CONFIGURATION REGISTERS**

*Table 31. Configuration Register Summary—Configuration Interface Functions (Address 0x00 to Address 0x11) (Continued)*

|      | Addr Name                      | Bits   | Bit 7                 | Bit 6                  | Bit 5           | Bit 4                     | Bit 3                      | Bit 2                         | Bit 1                               | Bit 0                           | Reset | R/W |
|------|--------------------------------|--------|-----------------------|------------------------|-----------------|---------------------------|----------------------------|-------------------------------|-------------------------------------|---------------------------------|-------|-----|
|      |                                |        |                       |                        | ACCESS          |                           |                            |                               |                                     |                                 |       |     |
| 0x11 | INTERFACE_<br>STATUS_A         | [7:0]  | NOT_<br>READY_<br>ERR |                        | RESERVED        | CLOCK_<br>COUNT_<br>ERR   | CRC_ERR                    | WR_TO_RD_<br>ONLY_REG_<br>ERR | REGISTER_<br>PARTIAL_<br>ACCESS_ERR | ADD<br>RESS_<br>INVALID_<br>ERR | 0x00  | R/W |
| 0x14 | DEVICE_<br>STATUS              | [7:0]  | FIFO_<br>FULL         | FIFO_<br>READ_<br>DONE | HI_STATUS       |                           | LO_STATUS POR_ANA_<br>FLAG | ADC_<br>CNV_ERR               | ROM_CRC_ERR                         | POR_<br>FLAG                    | 0x09  | R/W |
| 0x15 | ADC_DATA_<br>INTF_<br>CONFIG_A | [7:0]  | RE<br>SERVED          | RE<br>SERVED           | RESERVED        | INTF_<br>CHK_EN           | RESERVED                   | SPI_LVDS_<br>LANES            | RESERVED                            | DATA_<br>INTF_<br>MODE          | 0x40  | R/W |
| 0x16 | ADC_DATA_<br>INTF_<br>CONFIG_B | [7:0]  | LVDS_CNV_CLK_CNT      |                        |                 |                           | LVDS_<br>SELF_CLK_<br>MODE | LVDS_<br>MNC_EN               | RESERVED                            | LVDS_<br>CNV_EN                 | 0x00  | R/W |
| 0x17 | ADC_DATA_<br>INTF_<br>CONFIG_C | [7:0]  | LVDS_RX_<br>CURRENT   | LVDS_VOD<br>RESERVED   |                 |                           |                            |                               |                                     |                                 | 0x20  | R/W |
| 0x18 | PWR_CTRL                       | [7:0]  | RESERVED              |                        |                 |                           |                            |                               | ANA_DIG_<br>LDO_PD                  | INTF_<br>LDO_<br>PD             | 0x00  | R/W |
| 0x19 | GPIO_<br>CONFIG_A              | [7:0]  | GPIO_3_<br>DATA       | GPIO_2_<br>DATA        | GPIO_1_<br>DATA | GPIO_0_<br>DATA           | GPO_3_EN                   | GPO_2_EN                      | GPO_1_EN                            | GPO_0_<br>EN                    | 0x01  | R/W |
|      | 0x1A GPIO_<br>CONFIG_B         | [7:0]  | GPIO_1_SEL            |                        |                 |                           |                            | GPIO_0_SEL                    |                                     |                                 | 0x00  | R/W |
|      | 0x1B GPIO_<br>CONFIG_C         | [7:0]  |                       |                        | GPIO_3_SEL      |                           |                            | GPIO_2_SEL                    |                                     |                                 |       | R/W |
|      | 0x1C GENERAL_<br>CONFIG        | [7:0]  | INT_<br>EVENT_<br>EN  | HI_<br>ROUTE           | LO_ROUTE        | ADC_CNV_<br>ERR_<br>ROUTE |                            | RESERVED                      | FIFO_MODE                           |                                 | 0x00  | R/W |
|      | 0x1D FIFO_                     | [7:0]  |                       |                        |                 |                           | FIFO_WATERMARK[7:0]        |                               |                                     |                                 | 0x00  | R/W |
| 0x1E | WATERMARK                      | [15:8] | RE<br>SERVED          |                        |                 |                           | FIFO_WATERMARK[14:8]       |                               |                                     |                                 | 0x40  | R/W |
| 0x1F | EVENT_                         | [7:0]  |                       |                        |                 |                           | HYSTERESIS[7:0]            |                               |                                     |                                 | 0x00  | R/W |
| 0x20 | HYSTERESIS                     | [15:8] |                       |                        | RESERVED        |                           |                            |                               | HYSTERESIS[10:8]                    |                                 | 0x00  | R/W |
| 0x21 | EVENT_                         | [7:0]  |                       |                        |                 |                           | HI_THRESHOLD[7:0]          |                               |                                     |                                 | 0x00  | R/W |
| 0x22 | DETECTION_<br>HI               | [15:8] |                       |                        | RESERVED        |                           |                            |                               | HI_THRESHOLD[11:8]                  |                                 | 0x00  | R/W |
| 0x23 | EVENT_                         | [7:0]  |                       |                        |                 |                           | LO_THRESHOLD[7:0]          |                               |                                     |                                 | 0x00  | R/W |
| 0x24 | DETECTION_<br>LO               | [15:8] |                       |                        | RESERVED        |                           | LO_THRESHOLD[11:8]         |                               |                                     |                                 | 0x00  | R/W |
| 0x25 | OFFSET                         | [7:0]  |                       |                        |                 |                           | OFFSET[7:0]                |                               |                                     |                                 | 0x00  | R/W |
| 0x26 |                                | [15:8] |                       |                        | RESERVED        |                           |                            |                               | OFFSET[11:8]                        |                                 | 0x00  | R/W |
| 0x27 | GAIN                           | [7:0]  |                       |                        |                 |                           | GAIN[7:0]                  |                               |                                     |                                 | 0x00  | R/W |
| 0x28 |                                | [15:8] |                       |                        |                 | RESERVED                  |                            |                               | GAIN[9:8]                           |                                 | 0x02  | R/W |
| 0x29 | FILTER_<br>CONFIG              | [7:0]  | RE<br>SERVED          |                        |                 | SINC_DEC_RATE             |                            | RESERVED                      | FILTER_SEL                          |                                 | 0x00  | R/W |

**[analog.com](http://www.analog.com/en/index.html) Rev. 0 | 70 of 91**

#### <span id="page-70-0"></span>**CONFIGURATION REGISTERS**

#### **REGISTER DETAILS**

### **Interface Configuration A Register**

**Address: 0x00, Reset: 0x10, Name: INTERFACE\_CONFIG\_A**

![](_page_70_Figure_5.jpeg)

*Figure 105. Interface Configuration A Settings*

*Table 32. Bit Descriptions for INTERFACE\_CONFIG\_A*

| Bits  | Bit Name       | Description                                                                                                                                                                                                                                                                                                                                                                                   | Reset | Access |
|-------|----------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------|--------|
| 7     | SW_RESET       | First of the Two SW_RESET Bits. This bit appears in two locations in this register. Both locations must<br>be written to at the same time to trigger a software reset of the device. This action returns any previously<br>configured registers to their default settings, except for the ADDR_ASCENSION bit from the Interface<br>Configuration A Register, which keeps its previous value.  | 0x0   | R/W    |
|       |                | Only use this reset method once the ADC is in an idle state, where conversions are not being clocked, and<br>any existing conversions are completed.                                                                                                                                                                                                                                          |       |        |
| 6     | RESERVED       | Reserved. Write 0 to this bit.                                                                                                                                                                                                                                                                                                                                                                | 0x0   | R      |
| 5     | ADDR_ASCENSION | Determines Sequential Addressing Behavior.                                                                                                                                                                                                                                                                                                                                                    | 0x0   | R/W    |
|       |                | 0: Address is decremented by one when streaming.                                                                                                                                                                                                                                                                                                                                              |       |        |
|       |                | 1: Address is Incremented by one when streaming.                                                                                                                                                                                                                                                                                                                                              |       |        |
| 4     | SDO_ENABLE     | SDO Pin Enable.                                                                                                                                                                                                                                                                                                                                                                               | 0x1   | R      |
| [3:1] | RESERVED       | Reserved. Write 000 to these bits.                                                                                                                                                                                                                                                                                                                                                            | 0x0   | R      |
| 0     | SW_RESETX      | Second of the Two SW_RESET Bits. This bit appears in two locations in this register. Both locations must<br>be written to at the same time to trigger a software reset of the device. This action returns any previously<br>configured registers to their default settings, except for the ADDR_ASCENSION bit from the Interface<br>Configuration A Register, which keeps its previous value. | 0x0   | R/W    |
|       |                | Only use this reset method once the ADC is in an idle state, where conversions are not being clocked, and<br>any existing conversion are completed.                                                                                                                                                                                                                                           |       |        |

**[analog.com](http://www.analog.com/en/index.html) Rev. 0 | 71 of 91**

# <span id="page-71-0"></span>**CONFIGURATION REGISTERS**

# **Interface Configuration B Register**

**Address: 0x01, Reset: 0x00, Name: INTERFACE\_CONFIG\_B**

![](_page_71_Figure_4.jpeg)

*Figure 106. Additional Interface Configuration B Settings*

*Table 33. Bit Descriptions for INTERFACE\_CONFIG\_B*

| Bits  | Bit Name          | Description                                                                                                  | Reset | Access |
|-------|-------------------|--------------------------------------------------------------------------------------------------------------|-------|--------|
| 7     | SINGLE_INST       | Select Streaming or Single Instruction Mode.                                                                 | 0x0   | R/W    |
|       |                   | 0: Streaming mode is enabled. The address increments or decrements as successive data bytes are<br>received. |       |        |
|       |                   | 1: Single instruction mode is enabled.                                                                       |       |        |
| [6:4] | RESERVED          | Reserved. Write 0b000 to these bits.                                                                         | 0x0   | R      |
| 3     | SHORT_INSTRUCTION | Set the Instruction Phase Address to 7 or 15 bits.                                                           | 0x0   | R/W    |
|       |                   | 0: 15-Bit Addressing.                                                                                        |       |        |
|       |                   | 1: 7-Bit Addressing.                                                                                         |       |        |
| [2:0] | RESERVED          | Reserved. Write 0b000 to these bits.                                                                         | 0x0   | R      |

#### **Device Configuration Register**

**Address: 0x02, Reset: 0x00, Name: DEVICE\_CONFIG**

![](_page_71_Figure_10.jpeg)

*Figure 107. Device Configuration Register*

*Table 34. Bit Descriptions for DEVICE\_CONFIG*

| Bits  | Bit Name        | Description                             | Reset | Access |
|-------|-----------------|-----------------------------------------|-------|--------|
| [7:2] | RESERVED        | Reserved. Write 0b000000 to these bits. | 0x0   | R      |
| [1:0] | OPERATING_MODES | Power Modes.                            | 0x0   | R/W    |
|       |                 | 00: Normal Operating Mode.              |       |        |
|       |                 | 10: Standby Operating Mode.             |       |        |
|       |                 | 11: Sleep Mode.                         |       |        |

**[analog.com](http://www.analog.com/en/index.html) Rev. 0 | 72 of 91**

# **CONFIGURATION REGISTERS**

### **Chip Type Register**

**Address: 0x03, Reset: 0x07, Name: CHIP\_TYPE**

The chip type is used to identify the family of Analog Devices devices a given device belongs to. CHIP\_TYPE must be used in conjunction with the Product ID to uniquely identify a given product.

![](_page_72_Figure_5.jpeg)

*Figure 108. Chip Type Register*

*Table 35. Bit Descriptions for CHIP\_TYPE*

| Bits  | Bit Name  | Description    | Reset | Access |
|-------|-----------|----------------|-------|--------|
| [7:4] | RESERVED  | Reserved.      | 0x0   | R      |
| [3:0] | CHIP_TYPE | Precision ADC. | 0x7   | R      |

#### **Product ID Low Register**

**Address: 0x04, Reset: 0x00, Name: PRODUCT\_ID\_L**

This register is the low byte of the Product ID.

![](_page_72_Figure_12.jpeg)

*Figure 109. Product ID Low Register*

#### *Table 36. Bit Descriptions for PRODUCT\_ID\_L*

| Bits  | Bit Name        | Description                                                                                        | Reset | Access |  |
|-------|-----------------|----------------------------------------------------------------------------------------------------|-------|--------|--|
| [7:0] | PRODUCT_ID[7:0] | Product Identification. These bits are the device chip type/family. The PRODUCT_ID must be used in | 0x56  | R      |  |
|       |                 | conjunction with CHIP_TYPE to identify a product.                                                  |       |        |  |

**[analog.com](http://www.analog.com/en/index.html) Rev. 0 | 73 of 91**

# **CONFIGURATION REGISTERS**

### **Product ID High Register**

**Address: 0x05, Reset: 0x00, Name: PRODUCT\_ID\_H**

This register is the high byte of the Product ID.

![](_page_73_Figure_5.jpeg)

*Figure 110. Product ID High Register*

*Table 37. Bit Descriptions for PRODUCT\_ID\_H*

| Bits  | Bit Name         | Description                                                                                                                                                 | Reset | Access |
|-------|------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------|-------|--------|
| [7:0] | PRODUCT_ID[15:8] | Product Identification. These bits are the device chip type and family. The PRODUCT_ID must be used in<br>conjunction with CHIP_TYPE to identify a product. | 0x0   | R      |

# **Chip Grade Register**

**Address: 0x06, Reset: 0x02, Name: CHIP\_GRADE**

This register identifies product variations and device revisions.

![](_page_73_Figure_12.jpeg)

*Figure 111. Chip Grade Register*

*Table 38. Bit Descriptions for CHIP\_GRADE*

| Bits  | Bit Name        | Description                                                   | Reset | Access |
|-------|-----------------|---------------------------------------------------------------|-------|--------|
| [7:4] | GRADE           | Device Grade. These bits are the device performance grade.    | 0x0   | R      |
| [3:0] | DEVICE_REVISION | Device Revision. These bits are the device hardware revision. | 0x2   | R      |

#### **Scratch Pad Register**

**Address: 0x0A, Reset: 0x00, Name: SCRATCH\_PAD**

This register can be used to test writes and reads.

![](_page_73_Figure_19.jpeg)

*Figure 112. Scratch Pad Register*

*Table 39. Bit Descriptions for SCRATCH\_PAD*

| Bits  | Bit Name      | Description                                                                                             | Reset | Access |
|-------|---------------|---------------------------------------------------------------------------------------------------------|-------|--------|
| [7:0] | SCRATCH_VALUE | Software Scratchpad. Software can write to and read from this location without any device side effects. | 0x0   | R/W    |

**[analog.com](http://www.analog.com/en/index.html) Rev. 0 | 74 of 91**

# **CONFIGURATION REGISTERS**

# **SPI Revision Register**

**Address: 0x0B, Reset: 0x83, Name: SPI\_REVISION**

This register indicates the SPI revision.

![](_page_74_Figure_5.jpeg)

*Figure 113. SPI Revision Register*

*Table 40. Bit Descriptions for SPI\_REVISION*

| Bits  | Bit Name | Description                              | Reset | Access |
|-------|----------|------------------------------------------|-------|--------|
| [7:6] | SPI_TYPE | SPI Type. These bits always read as 0x2. | 0x2   | R      |
| [5:0] | VERSION  | SPI Version.                             | 0x3   | R      |
|       |          | 11: Revision 1.1.                        |       |        |

#### **Vendor ID Low Register**

**Address: 0x0C, Reset: 0x56, Name: VENDOR\_L**

This register is the low byte of the Vendor ID.

![](_page_74_Figure_12.jpeg)

*Figure 114. Vendor ID Low Register*

*Table 41. Bit Descriptions for VENDOR\_L*

| Bits  | Bit Name | Description               | Reset | Access |
|-------|----------|---------------------------|-------|--------|
| [7:0] | VID[7:0] | Analog Devices Vendor ID. | 0x56  | R      |

#### **Vendor ID High Register**

**Address: 0x0D, Reset: 0x04, Name: VENDOR\_H**

This register is the high byte of the Vendor ID.

![](_page_74_Figure_19.jpeg)

*Figure 115. Vendor ID High Register*

*Table 42. Bit Descriptions for VENDOR\_H*

| Bits  | Bit Name  | Description               | Reset | Access |
|-------|-----------|---------------------------|-------|--------|
| [7:0] | VID[15:8] | Analog Devices Vendor ID. | 0x4   | R      |

**[analog.com](http://www.analog.com/en/index.html) Rev. 0 | 75 of 91**

# **CONFIGURATION REGISTERS**

### **Stream Mode Register**

**Address: 0x0E, Reset: 0x00, Name: STREAM\_MODE**

This mode is not supported.

![](_page_75_Picture_5.jpeg)

*Figure 116. Stream Mode Register*

*Table 43. Bit Descriptions for STREAM\_MODE*

| Bits  | Bit Name   | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           | Reset | Access |
|-------|------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------|--------|
| [7:0] | LOOP_COUNT | Stream Mode Loop Counter. These bits set the data byte count before looping to the start address. When streaming<br>data, a nonzero value sets the number of data bytes written before the address loops back to the start address.<br>A maximum of 255 bytes can be written using this approach. A value of 0x00 disables the loop back so that<br>addressing wraps around at the upper and lower limits of the memory. After writing to this register, the loop value<br>applies only to the next SPI instruction and auto clears upon the end of that instruction. | 0x0   | R/W    |

#### **Transfer Configuration Register**

**Address: 0x0F, Reset: 0x00, Name: TRANSFER\_CONFIG**

This register controls how data moves between the controller and the target registers.

![](_page_75_Figure_12.jpeg)

*Figure 117. Transfer Configuration Register*

*Table 44. Bit Descriptions for TRANSFER\_CONFIG*

| Bits  | Bit Name               | Description                                                                          | Reset | Access |
|-------|------------------------|--------------------------------------------------------------------------------------|-------|--------|
| [7:3] | RESERVED               | Reserved. Write 0b00000 to these bits.                                               | 0x0   | R      |
| 2     | KEEP_STREAM_LENGTH_VAL | Keep Stream Length. When set, the loop counter does not reset on the CS rising edge. | 0x0   | R/W    |
| [1:0] | RESERVED               | Reserved. Write 0b00 to these bits.                                                  | 0x0   | R      |

**[analog.com](http://www.analog.com/en/index.html) Rev. 0 | 76 of 91**

# <span id="page-76-0"></span>**CONFIGURATION REGISTERS**

# **Interface Configuration C Register**

**Address: 0x10, Reset: 0x23, Name: INTERFACE\_CONFIG\_C**

This register contains additional interface configuration settings.

![](_page_76_Figure_5.jpeg)

*Figure 118. Interface Configuration C Register*

*Table 45. Bit Descriptions for INTERFACE\_CONFIG\_C*

| Bits  | Bit Name               | Description                                                                                                                                                                                                 | Reset | Access |
|-------|------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------|--------|
| [7:6] | CRC_ENABLE             | CRC Enable. These bits are written to enable or disable the use of CRC on the interface. The<br>CRC_ENABLE bits must also be written to with the inverted value of these bits for the CRC to be<br>enabled. | 0x0   | R/W    |
|       |                        | 0: CRC Disabled.                                                                                                                                                                                            |       |        |
|       |                        | 1: CRC Enabled.                                                                                                                                                                                             |       |        |
| 5     | STRICT_REGISTER_ACCESS | Multibyte Registers Must Be Read/Written in Full. When this mode is enabled, all bytes of a<br>multibyte register must be read/written in full.                                                             | 0x1   | R/W    |
|       |                        | 0: Normal Mode. No access restrictions.                                                                                                                                                                     |       |        |
|       |                        | 1: Strict Mode. Multibyte registers require all bytes accessed.                                                                                                                                             |       |        |
| 4     | SEND_STATUS            | Enables Sending of Status in 4-Wire Mode. When set, status information is sent by the device on<br>SDO during the instruction phase. When clear, no status is sent during the instruction phase.            | 0x0   | R/W    |
| [3:2] | ACTIVE_INTERFACE_MODE  | Configuration SPI Mode. These bits are the active mode the SPI operates in.                                                                                                                                 | 0x0   | R      |
| [1:0] | CRC_ENABLE             | Inverted CRC Enable. These bits must be written to with the inverted value of the CRC_ENABLE.                                                                                                               | 0x3   | R/W    |

**[analog.com](http://www.analog.com/en/index.html) Rev. 0 | 77 of 91**

# <span id="page-77-0"></span>**CONFIGURATION REGISTERS**

### **Interface Status A Register**

**Address: 0x11, Reset: 0x00, Name: INTERFACE\_STATUS\_A**

Status bits are set to 1 to indicate an active condition. These bits can be cleared by writing a 1 to the corresponding bit location.

![](_page_77_Figure_5.jpeg)

*Figure 119. Interface Status A Register*

*Table 46. Bit Descriptions for INTERFACE\_STATUS\_A*

| Bits  | Bit Name                    | Description                                                                                                                                                                                                                | Reset | Access |
|-------|-----------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------|--------|
| 7     | NOT_READY_ERR               | Device Not Ready for Transaction. This bit is set if the user attempts to execute an SPI<br>transaction before the completion of digital initialization.                                                                   | 0x0   | R/W1C  |
| [6:5] | RESERVED                    | Reserved. Write 0b00 to these bits.                                                                                                                                                                                        | 0x0   | R      |
| 4     | CLOCK_COUNT_ERR             | Clock Count Error. This bit is set when an incorrect number of clocks is detected in a<br>transaction.                                                                                                                     | 0x0   | R/W1C  |
| 3     | CRC_ERR                     | CRC Error. This bit is set when the SPI controller does not send a CRC or when the CRC<br>value calculated by the device does not match the value sent by the SPI controller.                                              | 0x0   | R/W1C  |
| 2     | WR_TO_RD_ONLY_REG_ERR       | Write to Read Only Register Error. This bit is set when the user attempts a write to a register<br>that is read only.                                                                                                      | 0x0   | R/W1C  |
| 1     | REGISTER_PARTIAL_ACCESS_ERR | Register Partial Access Error. This bit is set when a fewer than expected number of bytes<br>are read from or written to in a multibyte register access. This bit is only valid when strict<br>register access is enabled. | 0x0   | R/W1C  |
| 0     | ADDRESS_INVALID_ERR         | Invalid Address Error. This bit is set when the user tries to read from or write to a register<br>address outside of the allowed memory map space.                                                                         | 0x0   | R/W1C  |

**[analog.com](http://www.analog.com/en/index.html) Rev. 0 | 78 of 91**

# <span id="page-78-0"></span>**CONFIGURATION REGISTERS**

### **Device Status Register**

**Address: 0x14, Reset: 0x09, Name: DEVICE\_STATUS**

![](_page_78_Figure_4.jpeg)

*Figure 120. Device Status Register*

*Table 47. Bit Descriptions for DEVICE\_STATUS*

| Bits | Bit Name       | Description                                                                                                                                                                                                                                                                                   | Reset | Access |
|------|----------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------|--------|
| 7    | FIFO_FULL      | FIFO Full Status Flag.                                                                                                                                                                                                                                                                        | 0x0   | R      |
|      |                | 0: FIFO Not Full.                                                                                                                                                                                                                                                                             |       |        |
|      |                | 1: FIFO Full.                                                                                                                                                                                                                                                                                 |       |        |
| 6    | FIFO_READ_DONE | FIFO Read Done Flag.                                                                                                                                                                                                                                                                          | 0x0   | R      |
|      |                | 0: FIFO Read Not Done.                                                                                                                                                                                                                                                                        |       |        |
|      |                | 1: FIFO Read Done.                                                                                                                                                                                                                                                                            |       |        |
| 5    | HI_STATUS      | High Threshold Detection Status Flag. Writing 1 to this bit clears it.                                                                                                                                                                                                                        | 0x0   | R/W1C  |
|      |                | 0: High Threshold Event Not Detected.                                                                                                                                                                                                                                                         |       |        |
|      |                | 1: High Threshold Event Detected.                                                                                                                                                                                                                                                             |       |        |
| 4    | LO_STATUS      | Low Threshold Detection Status Flag. Writing 1 to this bit clears it.                                                                                                                                                                                                                         | 0x0   | R/W1C  |
|      |                | 0: Low Threshold Event Not Detected.                                                                                                                                                                                                                                                          |       |        |
|      |                | 1: Low Threshold Event Detected.                                                                                                                                                                                                                                                              |       |        |
| 3    | POR_ANA_FLAG   | POR Analog Status. Allows user to detect when an analog POR event occurs. An analog POR is triggered at<br>power-up or when the 1.1 V logic supply or ADC reference drops to less than the 2.7 threshold values or when<br>the user issues a software reset. Writing 1 to this bit clears it. | 0x1   | R/W1C  |
|      |                | 0: Analog POR Flag Cleared.                                                                                                                                                                                                                                                                   |       |        |
|      |                | 1: Analog POR Event Detected.                                                                                                                                                                                                                                                                 |       |        |
| 2    | ADC_CNV_ERR    | ADC Conversion Error Flag. Writing 1 to this bit clears it.                                                                                                                                                                                                                                   | 0x0   | R/W1C  |
|      |                | 0: ADC Conversion Okay.                                                                                                                                                                                                                                                                       |       |        |
|      |                | 1: ADC Conversion Error. The user has breached the minimum tCONV specification, and the conversion results<br>are invalid. The user must ensure that the correct clock timing specifications are met.                                                                                         |       |        |
| 1    | ROM_CRC_ERR    | ROM CRC/ECC Failure Flag.                                                                                                                                                                                                                                                                     | 0x0   | R      |
|      |                | 0: ROM CRC Check Okay.                                                                                                                                                                                                                                                                        |       |        |
|      |                | 1: ROM CRC/ECC Failure.                                                                                                                                                                                                                                                                       |       |        |
| 0    | POR_FLAG       | POR Status. Allows user to detect when a POR event occurs. A POR is triggered at power-up or when the 1.1<br>V logic supply drops to less than the 0.93 V threshold value or when the user issues a software reset. Writing 1<br>to this bit clears it.                                       | 0x1   | R/W1C  |
|      |                | 0: POR Flag Cleared.                                                                                                                                                                                                                                                                          |       |        |
|      |                | 1: POR Event Detected.                                                                                                                                                                                                                                                                        |       |        |

**[analog.com](http://www.analog.com/en/index.html) Rev. 0 | 79 of 91**

# <span id="page-79-0"></span>**CONFIGURATION REGISTERS**

# **ADC Data Interface Configuration A Register**

**Address: 0x15, Reset: 0x40, Name: ADC\_DATA\_INTF\_CONFIG\_A**

![](_page_79_Figure_4.jpeg)

*Figure 121. ADC Data Interface Configuration A Register*

*Table 48. Bit Descriptions for ADC\_DATA\_INTF\_CONFIG\_A*

| Bits | Bit Name       | Description                                                                                                                                                                                                          | Reset | Access |
|------|----------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------|--------|
| 7    | RESERVED       | Reserved. Write 0b0 to this bit.                                                                                                                                                                                     | 0x0   | R      |
| 6    | RESERVED       | Reserved. Always set this bit to 1.                                                                                                                                                                                  | 0x1   | R/W    |
| 5    | RESERVED       | Reserved. Write 0b0 to this bit.                                                                                                                                                                                     | 0x0   | R      |
| 4    | INTF_CHK_EN    | Output Fixed Test Pattern on ADC Data Interface (LVDS Only). ADC output is not available when this mode is<br>enabled. Fixed pattern = 20'b1010 1100 0101 1101 0110 (0xAC5D6).                                       | 0x0   | R/W    |
|      |                | 0: Test Pattern Disabled.                                                                                                                                                                                            |       |        |
|      |                | 1: Test Pattern Enabled.                                                                                                                                                                                             |       |        |
| 3    | RESERVED       | Reserved. Write 0b0 to this bit.                                                                                                                                                                                     | 0x0   | R      |
| 2    | SPI_LVDS_LANES | LVDS/SPI Lane Control. Determines the number of lanes that the ADC conversion data is clocked out on.                                                                                                                | 0x0   | R/W    |
|      |                | 0: One Lane Active.                                                                                                                                                                                                  |       |        |
|      |                | 1: Multiple Lanes Active (Two for LVDS and Four for the SPI Data Interface).                                                                                                                                         |       |        |
| 1    | RESERVED       | Reserved. Write 0b0 to this bit.                                                                                                                                                                                     | 0x0   | R      |
| 0    | DATA_INTF_MODE | Read Conversion Data Over SPI or LVDS. Acts as global LVDS enable, setting this bit to 1 powers down the<br>LVDS transmitters/receivers.                                                                             | 0x0   | R/W    |
|      |                | 0: Data Read Back Over LVDS.                                                                                                                                                                                         |       |        |
|      |                | 1: Data Read Back Over SPI Data Interface (DCS/DCLK). CLK+ is repurposed as the SPI data interface clock<br>(DCLK) for reading FIFO data, and CLK− is repurposed as the SPI chip select (DCS) for reading FIFO data. |       |        |

**[analog.com](http://www.analog.com/en/index.html) Rev. 0 | 80 of 91**

# <span id="page-80-0"></span>**CONFIGURATION REGISTERS**

### **ADC Data Interface Configuration B Register**

**Address: 0x16, Reset: 0x00, Name: ADC\_DATA\_INTF\_CONFIG\_B**

![](_page_80_Figure_4.jpeg)

*Figure 122. ADC Data Interface Configuration B Register*

*Table 49. Bit Descriptions for ADC\_DATA\_INTF\_CONFIG\_B*

| Bits  | Bit Name           | Description                                                                                                                                                                                                                                                                    | Reset | Access |
|-------|--------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------|--------|
| [7:4] | LVDS_CNV_CLK_CNT   | LVDS Clock Data Capture. Determines the negative edge of the LVDS clock that the MSB of the<br>conversion result is available in during conversion mode. Refer to the ADC Result Latency and LVDS<br>Interface Alignment section of further information on setting this value. | 0x0   | R/W    |
| 3     | LVDS_SELF_CLK_MODE | Enable/Disable LVDS Self Clock Mode.                                                                                                                                                                                                                                           | 0x0   | R/W    |
|       |                    | 0: Echo Clock Mode Enabled. LVDS DCO transmitter is powered up.                                                                                                                                                                                                                |       |        |
|       |                    | 1: Self Clock Mode Enabled. LVDS DCO transmitter is powered down .                                                                                                                                                                                                             |       |        |
| 2     | LVDS_MNC_EN        | Enable LVDS Manchester Encoding. Manchester encoding is only applied for LVDS read during<br>conversion mode in dual lane mode. This mode only operates with FILTER_SEL = 0, digital filter<br>disabled.                                                                       | 0x0   | R/W    |
|       |                    | 0: Manchester Encoding Disabled.                                                                                                                                                                                                                                               |       |        |
|       |                    | 1: Manchester Encoding Enabled.                                                                                                                                                                                                                                                |       |        |
| 1     | RESERVED           | Reserved. Write 0b0 to this bit.                                                                                                                                                                                                                                               | 0x0   | R      |
| 0     | LVDS_CNV_EN        | Configure CNV in LVDS Mode. Only applicable when LVDS interface is selected.                                                                                                                                                                                                   | 0x0   | R/W    |
|       |                    | 0: CNV Pin Configured in CMOS Mode.                                                                                                                                                                                                                                            |       |        |
|       |                    | 1: CNV Pin Configured in LVDS Mode.                                                                                                                                                                                                                                            |       |        |

#### **ADC Data Interface Configuration C Register**

**Address: 0x17, Reset: 0x20, Name: ADC\_DATA\_INTF\_CONFIG\_C**

![](_page_80_Figure_10.jpeg)

*Figure 123. ADC Data Interface Configuration C Register*

*Table 50. Bit Descriptions for ADC\_DATA\_INTF\_CONFIG\_C*

| Bits | Bit Name        | Description                                                        | Reset | Access |
|------|-----------------|--------------------------------------------------------------------|-------|--------|
| 7    | LVDS_RX_CURRENT | LVDS Receivers Current Mode. 1'b0 − 1× current. 1'b1 − 2x current. | 0x0   | R/W    |

**[analog.com](http://www.analog.com/en/index.html) Rev. 0 | 81 of 91**

# **CONFIGURATION REGISTERS**

*Table 50. Bit Descriptions for ADC\_DATA\_INTF\_CONFIG\_C (Continued)*

| Bits  | Bit Name | Description                                                                                                                                                                                                                                                                                                                  | Reset | Access |
|-------|----------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------|--------|
| [6:4] | LVDS_VOD | LVDS Differential Output Voltage. The valid entries are 0b001, 0b010, and 0b100 for the differential voltages<br>of ~185 mV, ~240 mV, and ~325 mV, respectively. Writing an invalid value resets the differential voltage to its<br>default setting of ~240 mV. However, user can read back the value written to these bits. | 0x2   | R/W    |
| [3:0] | RESERVED | Reserved. Write 0b0000 to these bits.                                                                                                                                                                                                                                                                                        | 0x0   | R      |

### **Power Control Register**

**Address: 0x18, Reset: 0x00, Name: PWR\_CTRL**

It is not recommended to write to this register.

![](_page_81_Figure_7.jpeg)

*Figure 124. Power Control Register*

*Table 51. Bit Descriptions for PWR\_CTRL*

| Bits  | Bit Name       | Description                                                                                                             | Reset | Access |
|-------|----------------|-------------------------------------------------------------------------------------------------------------------------|-------|--------|
| [7:2] | RESERVED       | Reserved. Write 0b000000 to these bits.                                                                                 | 0x0   | R      |
| 1     | ANA_DIG_LDO_PD | VDD11 LDO Disable. Enable or disable the LDO that powers the VDD11 rail. It is not recommended to<br>write to this bit. | 0x0   | R/W    |
|       |                | 0: LDO Enabled.                                                                                                         |       |        |
|       |                | 1: LDO Disabled.                                                                                                        |       |        |
| 0     | INTF_LDO_PD    | IOVDD LDO Disable. Enable or disable the LDO that powers the IOVDD rail. It is not recommended to<br>write to this bit. | 0x0   | R/W    |
|       |                | 0: LDO Enabled.                                                                                                         |       |        |
|       |                | 1: LDO Disabled.                                                                                                        |       |        |

**[analog.com](http://www.analog.com/en/index.html) Rev. 0 | 82 of 91**

# <span id="page-82-0"></span>**CONFIGURATION REGISTERS**

### **GPIO Configuration A Register**

**Address: 0x19, Reset: 0x01, Name: GPIO\_CONFIG\_A**

![](_page_82_Figure_4.jpeg)

*Figure 125. GPIO Configuration A Register*

*Table 52. Bit Descriptions for GPIO\_CONFIG\_A*

| Bits | Bit Name    | Description                        | Reset | Access |
|------|-------------|------------------------------------|-------|--------|
| 7    | GPIO_3_DATA | GPIO 3 Readback or Write Data.     | 0x0   | R/W    |
|      |             | 0: Write 0 to GPIO 3.              |       |        |
|      |             | 1: Write 1 to GPIO 3.              |       |        |
| 6    | GPIO_2_DATA | GPIO 2 Readback or Write Data.     | 0x0   | R/W    |
|      |             | 0: Write 0 to GPIO 2.              |       |        |
|      |             | 1: Write 1 to GPIO 2.              |       |        |
| 5    | GPIO_1_DATA | GPIO 1 Readback or Write Data.     | 0x0   | R/W    |
|      |             | 0: Write 0 to GPIO 1.              |       |        |
|      |             | 1: Write 1 to GPIO 1.              |       |        |
| 4    | GPIO_0_DATA | GPIO 0 Readback or Write Data.     | 0x0   | R/W    |
|      |             | 0: Write 0 to GPIO 0.              |       |        |
|      |             | 1: Write 1 to GPIO 0.              |       |        |
| 3    | GPO_3_EN    | GPIO 3 Output Enable.              | 0x0   | R/W    |
|      |             | 0: GPIO 3 Configured as an Input.  |       |        |
|      |             | 1: GPIO 3 Configured as an Output. |       |        |
| 2    | GPO_2_EN    | GPIO 2 Output Enable.              | 0x0   | R/W    |
|      |             | 0: GPIO 2 Configured as an Input.  |       |        |
|      |             | 1: GPIO 2 Configured as an Output. |       |        |
| 1    | GPO_1_EN    | GPIO 1 Output Enable.              | 0x0   | R/W    |
|      |             | 0: GPIO 1 Configured as an Input.  |       |        |
|      |             | 1: GPIO 1 Configured as an Output. |       |        |
| 0    | GPO_0_EN    | GPIO 0 Output Enable.              | 0x1   | R/W    |
|      |             | 0: GPIO 0 Configured as an Input.  |       |        |
|      |             | 1: GPIO 0 Configured as an Output. |       |        |
|      |             |                                    |       |        |

**[analog.com](http://www.analog.com/en/index.html) Rev. 0 | 83 of 91**

# <span id="page-83-0"></span>**CONFIGURATION REGISTERS**

# **GPIO Configuration B Register**

**Address: 0x1A, Reset: 0x00, Name: GPIO\_CONFIG\_B**

![](_page_83_Picture_4.jpeg)

*Figure 126. GPIO Configuration B Register*

*Table 53. Bit Descriptions for GPIO\_CONFIG\_B*

| Bits  | Bit Name   | Description                                      | Reset | Access |
|-------|------------|--------------------------------------------------|-------|--------|
| [7:4] | GPIO_1_SEL | GPIO 1 Write Select.                             | 0x0   | R/W    |
|       |            | 0000: Configuration SPI SDO Data.                |       |        |
|       |            | 0001: FIFO Full Flag.                            |       |        |
|       |            | 0010: FIFO Read Done Flag.                       |       |        |
|       |            | 0011: Filter Result Ready (Active Low).          |       |        |
|       |            | 0100: High Threshold Detect.                     |       |        |
|       |            | 0101: Low Threshold Detect.                      |       |        |
|       |            | 0110: Status Alert (Active Low).                 |       |        |
|       |            | 0111: GPIO Data.                                 |       |        |
|       |            | 1000: Filter Synchronization Input (Active Low). |       |        |
|       |            | 1001: External Event Trigger Input for FIFO.     |       |        |
|       |            | 1010: Do not use this setting.                   |       |        |
| [3:0] | GPIO_0_SEL | GPIO 0 Write Select.                             | 0x0   | R/W    |
|       |            | 0000: Configuration SPI SDO Data.                |       |        |
|       |            | 0001: FIFO Full Flag.                            |       |        |
|       |            | 0010: FIFO Read Done Flag.                       |       |        |
|       |            | 0011: Filter Result Ready (Active Low).          |       |        |
|       |            | 0100: High Threshold Detect.                     |       |        |
|       |            | 0101: Low Threshold Detect.                      |       |        |
|       |            | 0110: Status Alert (Active Low).                 |       |        |
|       |            | 0111: GPIO Data.                                 |       |        |
|       |            | 1000: Filter Synchronization Input (Active Low). |       |        |
|       |            | 1001: External Event Trigger Input for FIFO.     |       |        |
|       |            | 1010: Do not use this setting.                   |       |        |

**[analog.com](http://www.analog.com/en/index.html) Rev. 0 | 84 of 91**

# <span id="page-84-0"></span>**CONFIGURATION REGISTERS**

# **GPIO Configuration C Register**

**Address: 0x1B, Reset: 0x00, Name: GPIO\_CONFIG\_C**

![](_page_84_Figure_4.jpeg)

*Figure 127. GPIO Configuration C Register*

*Table 54. Bit Descriptions for GPIO\_CONFIG\_C*

| Bits  | Bit Name   | Description                                      | Reset | Access |
|-------|------------|--------------------------------------------------|-------|--------|
| [7:4] | GPIO_3_SEL | GPIO 3 Write Select.                             | 0x0   | R/W    |
|       |            | 0000: Configuration SPI SDO Data.                |       |        |
|       |            | 0001: FIFO Full Flag.                            |       |        |
|       |            | 0010: FIFO Read Done Flag.                       |       |        |
|       |            | 0011: Filter Result Ready (Active Low).          |       |        |
|       |            | 0100: High Threshold Detect.                     |       |        |
|       |            | 0101: Low Threshold Detect.                      |       |        |
|       |            | 0110: Status Alert (Active Low).                 |       |        |
|       |            | 0111: GPIO Data.                                 |       |        |
|       |            | 1000: Filter Synchronization Input (Active Low). |       |        |
|       |            | 1001: External Event Trigger Input for FIFO.     |       |        |
|       |            | 1010: Do not use this setting.                   |       |        |
| [3:0] | GPIO_2_SEL | GPIO 2 Write Select.                             | 0x0   | R/W    |
|       |            | 0000: Configuration SPI SDO Data.                |       |        |
|       |            | 0001: FIFO Full Flag.                            |       |        |
|       |            | 0010: FIFO Read Done Flag.                       |       |        |
|       |            | 0011: Filter Result Ready (Active Low).          |       |        |
|       |            | 0100: High Threshold Detect.                     |       |        |
|       |            | 0101: Low Threshold Detect.                      |       |        |
|       |            | 0110: Status Alert (Active Low).                 |       |        |
|       |            | 0111: GPIO Data.                                 |       |        |
|       |            | 1000: Filter Synchronization Input (Active Low). |       |        |
|       |            | 1001: External Event Trigger Input for FIFO.     |       |        |
|       |            | 1010: Do not use this setting.                   |       |        |

**[analog.com](http://www.analog.com/en/index.html) Rev. 0 | 85 of 91**

# <span id="page-85-0"></span>**CONFIGURATION REGISTERS**

### **General Configuration Register**

**Address: 0x1C, Reset: 0x00, Name: GENERAL\_CONFIG**

![](_page_85_Figure_4.jpeg)

*Figure 128. General Configuration Register*

*Table 55. Bit Descriptions for GENERAL\_CONFIG*

| Bits  | Bit Name          | Description                                                                                                                                    | Reset | Access |
|-------|-------------------|------------------------------------------------------------------------------------------------------------------------------------------------|-------|--------|
| 7     | INT_EVENT_EN      | Internal Event Detection Enable. ADC result or filtered data is only used for internal event detection after<br>this bit is set to 1.          | 0x0   | R/W    |
|       |                   | 0: Internal event detection is disabled.                                                                                                       |       |        |
|       |                   | 1: Internal event detection is enabled.                                                                                                        |       |        |
| 6     | HI_ROUTE          | High Detection Route. Allows high detection status to be used for FIFO event detection, status register,<br>and alert function (via the GPIO). | 0x0   | R/W    |
|       |                   | 0: Mask High Detection.                                                                                                                        |       |        |
|       |                   | 1: Route High Detection to Alert Pin, Status Register, and FIFO.                                                                               |       |        |
| 5     | LO_ROUTE          | Low Detection Route. Allows low detection status to be used for FIFO event detection, status register,<br>and alert function (via the GPIO).   | 0x0   | R/W    |
|       |                   | 0: Mask Low Detection.                                                                                                                         |       |        |
|       |                   | 1: Route Low Detection to Alert Pin, Status Register, and FIFO.                                                                                |       |        |
| 4     | ADC_CNV_ERR_ROUTE | ADC Conversion Error Route. Allows ADC conversion error status to be routed to the status register and<br>alert function (via the GPIO).       | 0x0   | R/W    |
|       |                   | 0: Mask ADC Conversion Error.                                                                                                                  |       |        |
|       |                   | 1: Route ADC Conversion Error to Alert Pin and Status Register.                                                                                |       |        |
| [3:2] | RESERVED          | Reserved. Write 0b0 to these bits.                                                                                                             | 0x0   | R      |
| [1:0] | FIFO_MODE         | Conversion Data FIFO Mode.                                                                                                                     | 0x0   | R/W    |
|       |                   | 00: FIFO Disabled.                                                                                                                             |       |        |
|       |                   | 01: Immediate Trigger Mode.                                                                                                                    |       |        |
|       |                   | 10: Event Trigger Capture, Read Latest WATERMARK.                                                                                              |       |        |
|       |                   | 11: Event Trigger Capture Mode, Read All FIFO.                                                                                                 |       |        |

**[analog.com](http://www.analog.com/en/index.html) Rev. 0 | 86 of 91**

# <span id="page-86-0"></span>**CONFIGURATION REGISTERS**

### **FIFO Watermark Register**

**Address: 0x1D and Address: 0x1E, Reset: 0x4000, Name: FIFO\_WATERMARK**

This is the watermark value. If the user writes a value <1, it is clipped at 1. If >16,384, clipped at 16,384.

![](_page_86_Figure_5.jpeg)

*Figure 129. FIFO Watermark Register*

#### *Table 56. Bit Descriptions for FIFO\_WATERMARK*

| Bits   | Bit Name       | Description                                                                                                                                  | Reset  | Access |
|--------|----------------|----------------------------------------------------------------------------------------------------------------------------------------------|--------|--------|
| 15     | RESERVED       | Reserved. Write 0b0 to this bit.                                                                                                             | 0x0    | R      |
| [14:0] | FIFO_WATERMARK | Number of Conversion to Capture in FIFO. In event trigger capture mode, read all FIFO, this value must<br>be set as a multiple of four only. | 0x4000 | R/W    |

### **Event Detection Hysteresis Configuration Register**

**Address: 0x20 and Address: 0x1F, Reset: 0x0000, Name: EVENT\_HYSTERESIS**

![](_page_86_Figure_11.jpeg)

*Figure 130. Event Detection Hysteresis Configuration Register*

#### *Table 57. Bit Descriptions for EVENT\_HYSTERESIS*

| Bits    | Bit Name   | Description                                                                                                                  | Reset | Access |
|---------|------------|------------------------------------------------------------------------------------------------------------------------------|-------|--------|
| [15:11] | RESERVED   | Reserved. Write 0b00000 to these bits.                                                                                       | 0x0   | R      |
| [10:0]  | HYSTERESIS | Hysteresis Value. Unsigned data format where LSB = 1.46484 mV. 0x000 represents 0 × LSB, and 0x7FF<br>represents 2047 × LSB. | 0x0   | R/W    |

**[analog.com](http://www.analog.com/en/index.html) Rev. 0 | 87 of 91**

### <span id="page-87-0"></span>**CONFIGURATION REGISTERS**

### **Event Detection High Threshold Configuration Register**

**Address: 0x21 and Address: 0x22, Reset: 0x0000, Name: EVENT\_DETECTION\_HI**

![](_page_87_Figure_4.jpeg)

*Figure 131. Event Detection High Threshold Configuration Register*

#### *Table 58. Bit Descriptions for EVENT\_DETECTION\_HI*

| Bits    | Bit Name     | Description                                                                                                                                  | Reset | Access |
|---------|--------------|----------------------------------------------------------------------------------------------------------------------------------------------|-------|--------|
| [15:12] | RESERVED     | Reserved. Write 0b0000 to these bits.                                                                                                        | 0x0   | R      |
| [11:0]  | HI_THRESHOLD | High Threshold Value. Twos complement data format where LSB = 1.46484 mV. 0x800 represents −2048 ×<br>LSB, and 0x7FF represents +2047 × LSB. | 0x0   | R/W    |

### **Event Detection Low Threshold Configuration Register**

**Address: 0x23 and Address: 0x24, Reset: 0x0000, Name: EVENT\_DETECTION\_LO**

![](_page_87_Figure_10.jpeg)

*Figure 132. Event Detection Low Threshold Configuration Register*

*Table 59. Bit Descriptions for EVENT\_DETECTION\_LO*

| Bits    | Bit Name     | Description                                                                                                                                 | Reset | Access |
|---------|--------------|---------------------------------------------------------------------------------------------------------------------------------------------|-------|--------|
| [15:12] | RESERVED     | Reserved. Write 0b0000 to these bits.                                                                                                       | 0x0   | R      |
| [11:0]  | LO_THRESHOLD | Low Threshold Value. Twos complement data format where LSB = 1.46484 mV. 0x800 represents −2048 ×<br>LSB, and 0x7FF represents +2047 × LSB. | 0x0   | R/W    |

#### **Offset Correction Register**

**Address: 0x25 and Address: 0x26, Reset: 0x0000, Name: OFFSET**

![](_page_87_Figure_16.jpeg)

*Figure 133. Offset Correction Register*

*Table 60. Bit Descriptions for OFFSET*

| Bits    | Bit Name | Description                                                                                                                                           | Reset | Access |
|---------|----------|-------------------------------------------------------------------------------------------------------------------------------------------------------|-------|--------|
| [15:12] | RESERVED | Reserved. Write 0b0000 to this bit field.                                                                                                             | 0x0   | R      |
| [11:0]  | OFFSET   | Offset Correction Coefficient. Twos complement data format where LSB = 0.00572 mV. 0x800 represents −2048 ×<br>LSB, and 0x7FF represents +2047 × LSB. | 0x0   | R/W    |

**[analog.com](http://www.analog.com/en/index.html) Rev. 0 | 88 of 91**

# <span id="page-88-0"></span>**CONFIGURATION REGISTERS**

### **Gain Correction Register**

**Address: 0x27 and Address: 0x28, Reset: 0x0200, Name: GAIN**

![](_page_88_Picture_4.jpeg)

*Figure 134. Gain Correction Register*

*Table 61. Bit Descriptions for GAIN*

| Bits    | Bit Name | Description                                                                                | Reset | Access |
|---------|----------|--------------------------------------------------------------------------------------------|-------|--------|
| [15:10] | RESERVED | Reserved. Write 0b000000 to these bits.                                                    | 0x0   | R      |
| [9:0]   | GAIN     | Gain Correction Coefficient                                                                | 0x200 | R/W    |
|         |          | GAIN = 0x3FF results in an overall system gain of 1.0 + 0.015594.                          |       |        |
|         |          | GAIN = 0x200 disables the gain correction function and allows for lower latency operation. |       |        |
|         |          | GAIN = 0x001 results in an overall system gain of 1.0 − 0.015594.                          |       |        |

**[analog.com](http://www.analog.com/en/index.html) Rev. 0 | 89 of 91**

# <span id="page-89-0"></span>**CONFIGURATION REGISTERS**

### **Filter Configuration Register**

**Address: 0x29, Reset: 0x00, Name: FILTER\_CONFIG**

![](_page_89_Picture_4.jpeg)

*Figure 135. Filter Configuration Register*

*Table 62. Bit Descriptions for FILTER\_CONFIG*

| Bits  | Bit Name      | Description                                                                                                                                                                                                                                  | Reset | Access |
|-------|---------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------|--------|
| 7     | RESERVED      | Reserved. Write 0b0 to this bit field.                                                                                                                                                                                                       | 0x0   | R      |
| [6:3] | SINC_DEC_RATE | Decimation Factor. These bits set the Sinc Decimation Factor N. The filter compensation block incurs an<br>additional 2× decimation. The total decimation for a selected filter is sinc1 = N, sinc5 = N, or sinc5 +<br>compensation = N × 2. | 0x0   | R/W    |
|       |               | For a selected filter, setting invalid values, outside of those specified here, will set the filter at the maximum<br>decimation rate                                                                                                        |       |        |
|       |               | 0000: N = 2.                                                                                                                                                                                                                                 |       |        |
|       |               | 0001: N = 4.                                                                                                                                                                                                                                 |       |        |
|       |               | 0010: N = 8.                                                                                                                                                                                                                                 |       |        |
|       |               | 0011: N = 16.                                                                                                                                                                                                                                |       |        |
|       |               | 0100: N = 32.                                                                                                                                                                                                                                |       |        |
|       |               | 0101: N = 64.                                                                                                                                                                                                                                |       |        |
|       |               | 0110: N = 128.                                                                                                                                                                                                                               |       |        |
|       |               | 0111: N = 256.                                                                                                                                                                                                                               |       |        |
|       |               | 1000: N = 512 (sinc1 only).                                                                                                                                                                                                                  |       |        |
|       |               | 1001: N = 1024 (sinc1 only).                                                                                                                                                                                                                 |       |        |
| 2     | RESERVED      | Reserved.                                                                                                                                                                                                                                    | 0x0   | R      |
| [1:0] | FILTER_SEL    | Filter Selection. To ensure the first filter result produces the correct data, when a user makes a change to the<br>filter selection, a reset must be issued via the GPIO pin configured for filter synchronization (FILTER_SYNC).           | 0x0   | R/W    |
|       |               | 00: Filter Disabled.                                                                                                                                                                                                                         |       |        |
|       |               | 01: Sinc1 Filter Selected.                                                                                                                                                                                                                   |       |        |
|       |               | 10: Sinc5 Filter Selected.                                                                                                                                                                                                                   |       |        |
|       |               | 11: Sinc5 + Compensation Filter Selected.                                                                                                                                                                                                    |       |        |

**[analog.com](http://www.analog.com/en/index.html) Rev. 0 | 90 of 91**

#### <span id="page-90-0"></span>**OUTLINE DIMENSIONS**

| Package Drawing (Option) | Package Type         | Package Description                        |
|--------------------------|----------------------|--------------------------------------------|
| BC-49-8                  | CSP BGA (Chip Scale) | 49-Ball Chip Scale Package Ball Grid Array |

For the latest package outline information and land patterns (footprints), go to [Package Index.](https://www.analog.com/en/resources/packaging-quality-symbols-footprints/package-index.html)

#### **ORDERING GUIDE**

| Model1         | Temperature Range | Package Description                                  | Packing Quantity | Package Option |
|----------------|-------------------|------------------------------------------------------|------------------|----------------|
| AD4086BBCZ     | −40°C to +85°C    | 49-Ball Chip Scale Package Ball Grid Array (CSP_BGA) | Tray, 490        | BC-49-8        |
| AD4086BBCZ-RL  | −40°C to +85°C    | 49-Ball Chip Scale Package Ball Grid Array (CSP_BGA) | Reel, 4000       | BC-49-8        |
| AD4086BBCZ-RL7 | −40°C to +85°C    | 49-Ball Chip Scale Package Ball Grid Array (CSP_BGA) | Reel, 1000       | BC-49-8        |

<sup>1</sup> Z = RoHS Compliant Part.

#### **Legal Terms and Conditions**

Information furnished by Analog Devices is believed to be accurate and reliable "as is". However, no responsibility is assumed by Analog Devices for its use, nor for any infringements of patents or other rights of third parties that may result from its use. Specifications subject to change without notice. No license is granted by implication or otherwise under any patent or patent rights of Analog Devices. Trademarks and registered trademarks are the property of their respective owners. All Analog Devices products contained herein are subject to release and availability.

**[analog.com](http://www.analog.com/en/index.html) Rev. 0 | 91 of 91**