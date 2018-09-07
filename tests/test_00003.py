import pydarknet2
import subprocess

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

def test_clone_000003_05(darknet_root, clone_url):
    # Build with GPU & cudNN
    dn = pydarknet2.Darknet(root=darknet_root)
    dn.build(gpu=True, cudnn=True, force=True)
    out = subprocess.check_output(["ldd", dn.exe]).decode("UTF-8")
    assert "libcudart" in out
    assert "libcudnn" in out
