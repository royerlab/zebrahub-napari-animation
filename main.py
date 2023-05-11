import napari
from napari_animation import Animation


def main() -> None:
    # toggle multiscale to tradeoff between speed and resolution
    MULTISCALE = False

    viewer = napari.Viewer()

    viewer.open(
        "http://public.czbiohub.org/royerlab/zebrahub/imaging/multi-view/ZMNS001.ome.zarr",
        plugin="napari-ome-zarr",
        rendering="attenuated_mip",
        gamma=0.7,
    )

    # disabling multiscale
    if not MULTISCALE:
        for channel in ("mezzo", "h2afva"):
            viewer.layers[channel].multiscale = False
            viewer.layers[channel].data = viewer.layers[channel].data[0]

    # aesthetics changes
    viewer.layers["h2afva"].colormap = "cyan"
    viewer.layers["h2afva"].contrast_limits = (50, 850)
    viewer.layers["mezzo"].colormap = "magenta"
    viewer.layers["mezzo"].contrast_limits = (50, 500)

    # making it 3D
    viewer.dims.ndisplay = 3

    # setting t = 0
    viewer.dims.set_point(0, 0)

    # starting recording
    animation = Animation(viewer)
    animation.capture_keyframe()

    # setting t = 220
    viewer.dims.set_point(0, 220)

    # updating contrasts
    viewer.layers["h2afva"].contrast_limits = (50, 2500)

    # ending recording
    animation.capture_keyframe(600)
    animation.animate('video.mp4', fps=60)


if __name__ == "__main__":
    main()
