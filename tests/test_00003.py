import pydarknet2

def test_build_000003_01(darknet_root, clone_url):
    # Clone a darknet directory.
    dn = pydarknet2.Darknet(root=darknet_root)
    dn.clone(clone_url=clone_url)

def test_clone_000003_02(darknet_root, clone_url):
    # Clone a darknet directory.
    dn = pydarknet2.Darknet(root=darknet_root)
    dn.build()
