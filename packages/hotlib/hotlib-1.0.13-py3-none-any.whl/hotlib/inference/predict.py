# Standard library imports
import os
from glob import glob
from pathlib import Path

# Third party imports
import numpy as np

from ..georeference import georeference
from ..utils import remove_files
from .utils import get_model, open_images, save_mask

IMAGE_SIZE = 256


os.environ["TF_CPP_MIN_LOG_LEVEL"] = "1"


def predict(
    checkpoint_path: str, data_path: str, image_dir: str, pred_dir: str
) -> None:
    """Predict masks for all images.

    Args:
        checkpoint_path: Path where the architecture and weights of the model can be found.
        data_path: Path of the directory where all the data are stored.
        image_dir: Name of the directory where the images are stored.
        pred_dir: Name of the directory where the predicted images will go.
    """
    pred_dir = Path(pred_dir)
    model = get_model(checkpoint_path)

    os.chdir(data_path)
    for sub_dir in os.listdir(image_dir):
        os.makedirs(pred_dir / sub_dir, exist_ok=True)
        image_paths = glob(f"{image_dir}/{sub_dir}/*.tif")
        images = open_images(image_paths)
        images = images.reshape(-1, IMAGE_SIZE, IMAGE_SIZE, 3)

        preds = model.predict(images)
        preds = np.where(preds > 0.5, 1, 0)

        for idx, path in enumerate(image_paths):
            path = Path(path)
            save_mask(
                preds[idx],
                str(pred_dir / sub_dir / f"{path.stem}.png"),
            )

        georeference(str(pred_dir), sub_dir, str(pred_dir), is_mask=True)
        remove_files(f"{pred_dir}/{sub_dir}/*.xml")
        remove_files(f"{pred_dir}/{sub_dir}/*.png")
