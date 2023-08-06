# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['asyncio_multilock']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'asyncio-multilock',
    'version': '0.1.0',
    'description': 'asyncio shared/exclusive mode lock',
    'long_description': '# asyncio-multilock\n\n[![asyncio-multilock](https://circleci.com/gh/phyrwork/asyncio-multilock/tree/main.svg?style=svg)](https://app.circleci.com/pipelines/github/phyrwork/asyncio-multilock?branch=main)\n\n`asyncio_multilock` provides `MultiLock`, an `asyncio` based lock with built-in\nshared/exclusive mode semantics.\n\n`MultiLock.locked` can be in one of three states:\n\n1. `None` - not locked;\n2. `MultiLockType.SHARED` - acquired one or more times in shared mode;\n3. `MultiLockType.EXCLUSIVE` - acquired one time in exclusive mode.\n\nWhen a lock is acquired, a `Hashable` handle is returned which uniquely identifies\nthe acquisition. This handle is used to release the acquisition.\n\n```python\nfrom asyncio import create_task, sleep\nfrom asyncio_multilock import MultiLock, MultiLockType\n\nlock = MultiLock()\nassert not lock.locked\n\nshared1 = await lock.acquire(MultiLockType.SHARED)\nassert lock.locked is MultiLockType.SHARED\n\nshared2 = await lock.acquire(MultiLockType.SHARED)\n\nasync def wait_release_shared(delay: float) -> None:\n    await sleep(delay)\n    lock.release(shared1)\n    lock.release(shared2)\ncreate_task(wait_release_shared(3))\n\n# Acquisition context manager.\nasync with lock.context(MultiLockType.EXCLUSIVE) as exclusive:\n    # Blocked for 3 seconds.\n    assert lock.locked is MultiLockType.EXCLUSIVE\n```\n\nThe lock can also be acquired synchronously, returning no handle if the acquisition\nfails.\n\n```python\nfrom asyncio_multilock import MultiLock, MultiLockType\n\nlock = MultiLock()\nassert not lock.locked\n\nshared = lock.acquire_nowait(MultiLockType.SHARED)\nassert shared\n\nexclusive = lock.acquire_nowait(MultiLockType.EXCLUSIVE)\nassert not exclusive\n\nassert lock.locked is MultiLockType.SHARED\n```\n\nThe lock can also be monitored for when a given lock type is next acquirable.\n\n```python\nfrom asyncio_multilock import MultiLock, MultiLockType\n\nlock = MultiLock()\n\nasync with lock.notify(MultiLockType.SHARED) as event:\n    await event.wait()\n    print("shared lock is acquirable")\n    event.clear()\n```\n',
    'author': 'Connor Newton',
    'author_email': 'connor@ifthenelse.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
