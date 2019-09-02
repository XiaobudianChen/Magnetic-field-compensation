# Magnetic-field-compensation
## Abstract
Compensate the external magnetic field with active feedback and output the result as a file.
## Introduction
- The magnitude of the magnetic field is detected by a fluxgate([Mag-03IEB70 of Bartington instrumrnts](www.bartington.com)), whose output is a voltage data.
- Using a multimeter ([Agilent 34410A](https://github.com/XiaobudianChen/Magnetic-field-compensation/blob/master/34410A_11A_SCPI_Reference.chm)) to detect the voltage signal to obtain a relative magnetic field value
- The coil is energized by a precision current source ([QL Series II](https://github.com/XiaobudianChen/Magnetic-field-compensation/blob/master/QL%20Series%20II%20-%20Instruction%20Manual%20-%20Iss%208.pdf)), and the current is controlled by the program so that the voltmeter measures 0, that is, the magnetic field is zero (or a specific value).
