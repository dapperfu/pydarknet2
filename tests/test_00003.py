import pydarknet2
import subprocess
import os
import pytest

def test_build_000003_01(darknet_root, clone_url):
    # Clone a darknet directory.
    dn = pydarknet2.Darknet(root=darknet_root)
    dn.clone(clone_url=clone_url)

def test_clone_000003_02(darknet_root, clone_url):
    # Build without opencv or openmp.
    dn = pydarknet2.Darknet(root=darknet_root)
    dn.build(opencv=False, openmp=False, force=True)
    out = subprocess.check_output(["ldd", dn.exe]).decode("UTF-8")
    assert "openmp" not in out
    assert "opencv" not in out

def test_clone_000003_04(darknet_root, clone_url):
    # Build with opencv or openmp.
    dn = pydarknet2.Darknet(root=darknet_root)
    dn.build(opencv=True, openmp=True, force=True)
    out = subprocess.check_output(["ldd", dn.exe]).decode("UTF-8")
    assert "openmp" in out
    assert "opencv" in out

@pytest.mark.skipif(not os.path.exists("/usr/local/cuda"), reason="Requires CUDA to be installed.")
@pytest.mark.skipif(not os.path.exists("/usr/local/cuda/lib64/libcudnn.so"), reason="Requires cudNN to be installed.")
def test_clone_000003_05(darknet_root, clone_url):
    # Build with GPU & cudNN if available.
    dn = pydarknet2.Darknet(root=darknet_root)

    # Hack/Workaround.
    os.environ["PATH"] = os.environ["PATH"]+os.pathsep+"/usr/local/cuda/bin"
    if "LD_LIBRARY_PATH" in os.environ:
        os.environ["LD_LIBRARY_PATH"] = os.environ["LD_LIBRARY_PATH"]+os.pathsep+"/usr/local/cuda/lib64"
    else:
        os.environ["LD_LIBRARY_PATH"] = "/usr/local/cuda/lib64"

    dn.build(gpu=True, cudnn=True, force=True)
    out = subprocess.check_output(["ldd", dn.exe]).decode("UTF-8")
    assert "libcudart" in out
    assert "libcudnn" in out
