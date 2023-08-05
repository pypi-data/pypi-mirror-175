# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['gcnn_dmri', 'gcnn_dmri.example_scripts']

package_data = \
{'': ['*']}

install_requires = \
['antiprism-python>=0.1.3,<0.2.0',
 'dipy>=1.5.0,<2.0.0',
 'matplotlib>=3.6.0,<4.0.0',
 'nibabel>=4.0.2,<5.0.0',
 'numpy>=1.23.0,<2.0.0',
 'scipy>=1.9.1,<2.0.0',
 'stripy>=2.1.0,<3.0.0',
 'torch>=1.7.1,<2.0.0']

setup_kwargs = {
    'name': 'gcnn-dmri',
    'version': '0.1.0',
    'description': 'Graph-equivariant CNNs for diffusion MRI',
    'long_description': '# Gauge equivariant CNNs for Diffusion MRI (gcnn_dmri)\n\n[![PyPI](https://img.shields.io/pypi/v/gcnn_dmri?style=flat-square)](https://pypi.python.org/pypi/gcnn_dmri/)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/gcnn_dmri?style=flat-square)](https://pypi.python.org/pypi/gcnn_dmri/)\n[![PyPI - License](https://img.shields.io/pypi/l/gcnn_dmri?style=flat-square)](https://pypi.python.org/pypi/gcnn_dmri/)\n[![Coookiecutter - Wolt](https://img.shields.io/badge/cookiecutter-Wolt-00c2e8?style=flat-square&logo=cookiecutter&logoColor=D4AA00&link=https://github.com/woltapp/wolt-python-package-cookiecutter)](https://github.com/woltapp/wolt-python-package-cookiecutter)\n\n---\n\n<img src=\'https://github.com/uhussai7/images/blob/main/rectangle.svg\' align=\'right\' width=\'240\'>\n\ngcnn_dmri incorporates gauge equivariance into cnns designed to process diffusion MRI (dMRI) data. The dmri signal is realized on an antipodally identified sphere, i.e the real projective space <img src=\'https://latex.codecogs.com/svg.image?\\mathbb{R}P^2\'>. Inspired by <a href=https://arxiv.org/pdf/1902.04615.pdf>Cohen et al.</a> we model this \'half-sphere\' as the top of an icosahedron. Interestingly, invoking the correct padding naturally leads us to use the full dihedral group, <img src=\'https://latex.codecogs.com/svg.image?D_6\'> , to include reflections in addition to rotations of the hexagon, as shown in the image on the right. Here we show the application of such gauge equivariant layers to de-noising <a href =\'https://www.humanconnectome.org/\'>Human Connectome Project</a> dMRI data limited to six gradient directions, a problem similar to the work of <a href=\'https://www.sciencedirect.com/science/article/pii/S1053811920305036\'>Tian et al. </a>\n\n### Data preparation\n- Select random subject id\'s for training and testing, one approach is shown in [`dataHandling/subject_list_generator.py`](dataHandling/subject_list_generator.py).\n- Similar to <a href=\'https://www.sciencedirect.com/science/article/pii/S1053811920305036\'>Tian et al. </a> we use a mask that avoids CSF. For this we need a grey matter and a white matter mask, which can be made from <a href=\'https://surfer.nmr.mgh.harvard.edu/fswiki/mri_binarize\'> `mri_binarize` </a> with the flags `--all-wm` and `--gm` respectively.\n- Further steps are shown in [niceData.py](niceData.py):\n    - `make_freesurfer_masks` runs the shell script to make the mask mentioned above.\n    - `make_loss_mask_and_structural` finalizes the mask, T1 and T2 images with the correct padding and resolution.\n    - `make_diffusion` creates diffusion volumes with fewer gradient directions, directions are choosen in the sequence of the aquisition and then cut off at desired number.\n    - `dtifit_on_directions` runs <a href=\'https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/FDT/UserGuide\'> `dtifit` </a> on the new diffusion volumes with fewer directions.\n    - We obtain the following folder structure:\n      ```\n        ── <training/testing>\n            ├── <subject_id>\n            │   ├── diffusion\n            │   │   └── <# of gradient directions>\n            │   │       ├── diffusion\n            │   │       │   ├── bvals\n            │   │       │   ├── bvecs\n            │   │       │   ├── data.nii.gz\n            │   │       │   ├── nodif_brain_mask.nii.gz\n            │   │       │   └── S0mean.nii.gz\n            │   │       └── dtifit\n            │   │           ├── dtifit_< >.nii.gz\n            │   ├── freesurfer_mask\n            │   │   ├── mask_all_wm.nii.gz\n            │   │   └── mask_gm.nii.gz\n            │   ├── masks\n            │   │   ├── mask_all_wm.nii.gz\n            │   │   ├── mask_gm.nii.gz\n            │   │   └── mask.nii.gz\n            │   └── structural\n            │       ├── T1.nii.gz\n            │       └── T2.nii.gz\n      ```\n### Training\nSimilar to <a href=\'https://www.sciencedirect.com/science/article/pii/S1053811920305036\'>Tian et al. </a> (and references therein) we use a residual network architecture but with the addition of gauge equivariant convolutions on the half icosahedron. The training script with the parameters used is [`training_script.py`](training_script.py). Note that structural mri images (`T1.nii.gz` and `T2.nii.gz`) are also used as inputs.\n\n### Predictions\nPredictions can be performed with the script [`predicting_script.py`](predicting_script.py). This will create a diffusion volume file, `data_network.nii.gz` along with `bvecs_network` and `bvals_network`, upon which one may perform `dtifit`. Following are some results of the denoising, the left grey images are fractional anistropy and right colored images are the `V1` vector:\n\n<p align="center" width="100%">\n    <img src=\'https://github.com/uhussai7/images/blob/main/gcnn_dmri.png\' width=\'960\'>\n</p>\n\n---\n\n**Documentation**: [https://akhanf.github.io/gcnn_dmri](https://akhanf.github.io/gcnn_dmri)\n\n**Source Code**: [https://github.com/akhanf/gcnn_dmri](https://github.com/akhanf/gcnn_dmri)\n\n**PyPI**: [https://pypi.org/project/gcnn_dmri/](https://pypi.org/project/gcnn_dmri/)\n\n---\n\nGraph-equivariant CNNs for diffusion MRI\n\n## Installation\n\n```sh\npip install gcnn_dmri\n```\n\n## Development\n\n* Clone this repository\n* Requirements:\n  * [Poetry](https://python-poetry.org/)\n  * Python 3.7+\n* Create a virtual environment and install the dependencies\n\n```sh\npoetry install\n```\n\n* Activate the virtual environment\n\n```sh\npoetry shell\n```\n\n### Testing\n\n```sh\npytest\n```\n\n### Documentation\n\nThe documentation is automatically generated from the content of the [docs directory](./docs) and from the docstrings\n of the public signatures of the source code. The documentation is updated and published as a [Github project page\n ](https://pages.github.com/) automatically as part each release.\n\n### Releasing\n\nTrigger the [Draft release workflow](https://github.com/akhanf/gcnn_dmri/actions/workflows/draft_release.yml)\n(press _Run workflow_). This will update the changelog & version and create a GitHub release which is in _Draft_ state.\n\nFind the draft release from the\n[GitHub releases](https://github.com/akhanf/gcnn_dmri/releases) and publish it. When\n a release is published, it\'ll trigger [release](https://github.com/akhanf/gcnn_dmri/blob/master/.github/workflows/release.yml) workflow which creates PyPI\n release and deploys updated documentation.\n\n### Pre-commit\n\nPre-commit hooks run all the auto-formatters (e.g. `black`, `isort`), linters (e.g. `mypy`, `flake8`), and other quality\n checks to make sure the changeset is in good shape before a commit/push happens.\n\nYou can install the hooks with (runs for each commit):\n\n```sh\npre-commit install\n```\n\nOr if you want them to run only for each push:\n\n```sh\npre-commit install -t pre-push\n```\n\nOr if you want e.g. want to run all checks manually for all files:\n\n```sh\npre-commit run --all-files\n```\n\n---\n\nThis project was generated using the [wolt-python-package-cookiecutter](https://github.com/woltapp/wolt-python-package-cookiecutter) template.\n',
    'author': 'Uzair Hussain',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://akhanf.github.io/gcnn_dmri',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)
