import { Composition, registerRoot, useCurrentFrame } from "remotion";
import { Format, SIZES, Slide, SlideData } from "./Slide";

type PostProps = { format: Format; slides: SlideData[] };

const Post = ({ format, slides }: PostProps) => {
  const index = useCurrentFrame();
  return <Slide slide={slides[index]} index={index} count={slides.length} format={format} />;
};

const sample: PostProps = {
  format: "carousel",
  slides: [
    { kind: "cover", title: "Board game night", text: "Friday, 6 PM", items: [], photo: null },
    { kind: "final", title: "See you there!", text: "Save this and send it to a friend", items: [], photo: null },
  ],
};

registerRoot(() => (
  <Composition
    id="Post"
    component={Post}
    width={SIZES.carousel.width}
    height={SIZES.carousel.height}
    fps={30}
    durationInFrames={1}
    defaultProps={sample}
    calculateMetadata={({ props }) => ({ durationInFrames: props.slides.length, ...SIZES[props.format] })}
  />
));
