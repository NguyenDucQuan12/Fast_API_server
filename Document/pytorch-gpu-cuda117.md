Check if CUDA is available by torch:

```py
import torch

def check_cuda():
    print(torch.version.cuda)
    cuda_is_ok = torch.cuda.is_available()
    print(f"CUDA Enabled: {cuda_is_ok}")
```

Get CUDA version:

```sh
nvidia-smi
```

```
Sun Aug 13 01:27:00 2023
+---------------------------------------------------------------------------------------+
| NVIDIA-SMI 531.79                 Driver Version: 531.79       CUDA Version: 12.1     |
|-----------------------------------------+----------------------+----------------------+
| GPU  Name                      TCC/WDDM | Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf            Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
|                                         |                      |               MIG M. |
|=========================================+======================+======================|
|   0  NVIDIA GeForce RTX 2060 S...  WDDM | 00000000:01:00.0  On |                  N/A |
| 40%   37C    P8               35W / 105W|   1762MiB /  8192MiB |     23%      Default |
|                                         |                      |                  N/A |
+-----------------------------------------+----------------------+----------------------+
```

So the CUDA version for our driver is `12.1`.
But currently (2023.08.13), the latest pytorch only supports up to CUDA 11.8,
so we need to download and install an older CUDA version.

I recommend Download and Install CUDA 11.7:

* CUDA Toolkit Archive | NVIDIA Developer
  * https://developer.nvidia.com/cuda-toolkit-archive
  * https://developer.nvidia.com/cuda-11-7-0-download-archive?target_os=Windows&target_arch=x86_64&target_version=10&target_type=exe_local

Now we could use `nvcc` to check CUDA version:

```sh
nvcc --version
```

```
nvcc: NVIDIA (R) Cuda compiler driver
Copyright (c) 2005-2022 NVIDIA Corporation
Built on Tue_May__3_19:00:59_Pacific_Daylight_Time_2022
Cuda compilation tools, release 11.7, V11.7.64
Build cuda_11.7.r11.7/compiler.31294372_0
```

Add following paths to environments path variables: (The installation would add them by default)

```
C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.7\bin
C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.7\libnvvp
```

Run following commands to install Python torch with CUDA enabled:

```sh
python -m pip uninstall torch
python -m pip cache purge

# Use 11.7, it should be compatible
python -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu117

# If want to use preview version of torch with CUDA 12.1
# python -m pip install torch torchvision --pre -f https://download.pytorch.org/whl/nightly/cu121/torch_nightly.html
```

## Issues

If `torch.version.cuda` always returns `None`, this means the installed PyTorch library was not built with CUDA support.
So we need to choose another version of torch.

```
python -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu117
# python -m pip install torch==2.0.0+cu117 torchvision==0.15.1+cu117 torchaudio==2.0.1 --index-url https://download.pytorch.org/whl/cu117
```

Or your CUDA version is too new that torch has not supported, so you need to choose another CUDA version to download and install.
I recommend to use 11.7, while 12.1 is too new:
* CUDA Toolkit 11.7 Downloads | NVIDIA Developer
  * https://developer.nvidia.com/cuda-11-7-0-download-archive

**References:**
* Install pytorch with Cuda 12.1 - PyTorch Forums
  * https://discuss.pytorch.org/t/install-pytorch-with-cuda-12-1/174294/17
* Pytorch installation with CUDA 12.1 - Reddit
  * https://www.reddit.com/r/pytorch/comments/11z9vkf/comment/jm5g09k/?utm_source=share&utm_medium=web2x&context=3

* Start Locally | PyTorch
  * https://pytorch.org/get-started/locally/
* Previous PyTorch Versions | PyTorch
  * https://pytorch.org/get-started/previous-versions/