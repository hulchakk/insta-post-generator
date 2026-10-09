import React from "react";
import { AbsoluteFill, Img, staticFile } from "remotion";

export type Format = "carousel" | "story";

export type SlideData = {
  kind: "cover" | "info" | "facts" | "final";
  title: string;
  text: string;
  items: string[];
  photo: string | null;
};

export const SIZES: Record<Format, { width: number; height: number }> = {
  carousel: { width: 1080, height: 1350 },
  story: { width: 1080, height: 1920 },
};
const PADDING: Record<Format, string> = { carousel: "80px 80px", story: "250px 70px 340px" };

const INK = "#1B1B1F";
const FONT = '"Inter", "Helvetica Neue", Arial, sans-serif';
const COLORS = [
  { bg: "#FFF6CC", pop: "#FFD93D" },
  { bg: "#FFE3EF", pop: "#FF8FBF" },
  { bg: "#DDF7E9", pop: "#6FDCA6" },
  { bg: "#DCEEFF", pop: "#7CC3FF" },
  { bg: "#ECE4FF", pop: "#B9A2FF" },
];

const outline = `5px solid ${INK}`;
const sticker = { border: outline, boxShadow: `10px 10px 0 ${INK}` };
const card: React.CSSProperties = { ...sticker, background: "#fff", borderRadius: 44, padding: "48px 52px" };

const fitFontSize = (text: string, sizes: [number, number, number]) =>
  text.length <= 18 ? sizes[0] : text.length <= 36 ? sizes[1] : sizes[2];

const Pill = ({ children, color, size = 36 }: { children: React.ReactNode; color: string; size?: number }) => (
  <div
    style={{
      display: "inline-block",
      alignSelf: "flex-start",
      background: color,
      border: outline,
      borderRadius: 999,
      padding: "8px 28px",
      fontSize: size,
      fontWeight: 800,
    }}
  >
    {children}
  </div>
);

const Photo = ({ src, height }: { src: string; height: number | string }) => (
  <Img src={staticFile(src)} style={{ ...sticker, width: "100%", height, objectFit: "cover", borderRadius: 44 }} />
);

const Dots = ({ index, count, pop }: { index: number; count: number; pop: string }) => (
  <div style={{ display: "flex", gap: 14 }}>
    {Array.from({ length: count }, (_, i) => (
      <div
        key={i}
        style={{
          width: i === index ? 72 : 24,
          height: 24,
          borderRadius: 12,
          border: outline,
          background: i === index ? pop : "#fff",
        }}
      />
    ))}
  </div>
);

const Arrow = ({ pop }: { pop: string }) => (
  <div
    style={{
      ...sticker,
      width: 96,
      height: 96,
      borderRadius: "50%",
      background: pop,
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      fontSize: 56,
      fontWeight: 900,
    }}
  >
    →
  </div>
);

const Cover = ({ slide, pop }: { slide: SlideData; pop: string }) => (
  <>
    {slide.photo && (
      <div style={{ flex: 1, minHeight: 0 }}>
        <Photo src={slide.photo} height="100%" />
      </div>
    )}
    <div style={{ ...card, position: "relative", marginTop: slide.photo ? 48 : "auto", marginBottom: slide.photo ? 0 : "auto" }}>
      {slide.text && (
        <div style={{ position: "absolute", top: -34, left: 36, transform: "rotate(-3deg)" }}>
          <Pill color={pop}>{slide.text}</Pill>
        </div>
      )}
      <div style={{ fontSize: fitFontSize(slide.title, [130, 110, 90]), fontWeight: 900, lineHeight: 1.02, marginTop: slide.text ? 16 : 0 }}>
        {slide.title}
      </div>
    </div>
  </>
);

const Info = ({ slide, pop }: { slide: SlideData; pop: string }) => (
  <>
    {slide.photo && <Photo src={slide.photo} height={380} />}
    <div style={{ ...card, display: "flex", flexDirection: "column", gap: 28, marginTop: slide.photo ? 48 : "auto", marginBottom: slide.photo ? 0 : "auto" }}>
      <div style={{ fontSize: fitFontSize(slide.title, [92, 80, 66]), fontWeight: 900, lineHeight: 1.05 }}>{slide.title}</div>
      {slide.text && <div style={{ fontSize: 44, fontWeight: 500, lineHeight: 1.3 }}>{slide.text}</div>}
      {slide.items.map((item, i) => (
        <div key={i} style={{ display: "flex", alignItems: "center", gap: 24 }}>
          <div
            style={{
              flex: "none",
              width: 64,
              height: 64,
              borderRadius: "50%",
              background: pop,
              border: outline,
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              fontSize: 34,
              fontWeight: 900,
            }}
          >
            {i + 1}
          </div>
          <div style={{ fontSize: 42, fontWeight: 700, lineHeight: 1.2 }}>{item}</div>
        </div>
      ))}
    </div>
  </>
);

const Facts = ({ slide, pop }: { slide: SlideData; pop: string }) => (
  <div style={{ margin: "auto 0", display: "flex", flexDirection: "column", gap: 40 }}>
    <div style={{ fontSize: fitFontSize(slide.title, [104, 90, 74]), fontWeight: 900, lineHeight: 1.05 }}>{slide.title}</div>
    <div style={{ ...card, display: "flex", flexDirection: "column", gap: 34 }}>
      {slide.items.map((item, i) => {
        const [label, ...rest] = item.split(":");
        const value = rest.length ? rest.join(":").trim() : label;
        return (
          <div key={i} style={{ display: "flex", flexDirection: "column", gap: 12 }}>
            {rest.length > 0 && <Pill color={pop} size={30}>{label.trim()}</Pill>}
            <div style={{ fontSize: 54, fontWeight: 800, lineHeight: 1.1 }}>{value}</div>
          </div>
        );
      })}
    </div>
  </div>
);

const Final = ({ slide, pop }: { slide: SlideData; pop: string }) => (
  <div style={{ margin: "auto 0", display: "flex", flexDirection: "column", gap: 40 }}>
    {slide.photo && <Photo src={slide.photo} height={360} />}
    <div style={{ ...card, background: pop, transform: "rotate(-2deg)" }}>
      <div style={{ fontSize: fitFontSize(slide.title, [110, 96, 78]), fontWeight: 900, lineHeight: 1.04 }}>{slide.title}</div>
    </div>
    {slide.text && <div style={{ fontSize: 46, fontWeight: 600, lineHeight: 1.3 }}>{slide.text}</div>}
    <div style={{ display: "flex", flexWrap: "wrap", gap: 20 }}>
      {slide.items.map((item, i) => (
        <Pill key={i} color="#fff" size={38}>{item}</Pill>
      ))}
    </div>
  </div>
);

const BODIES = { cover: Cover, info: Info, facts: Facts, final: Final };

export const Slide = ({ slide, index, count, format }: { slide: SlideData; index: number; count: number; format: Format }) => {
  const { bg, pop } = COLORS[index % COLORS.length];
  const Body = BODIES[slide.kind];
  return (
    <AbsoluteFill
      style={{ background: bg, padding: PADDING[format], boxSizing: "border-box", fontFamily: FONT, color: INK, display: "flex", flexDirection: "column" }}
    >
      <div style={{ position: "absolute", top: -120, right: -120, width: 420, height: 420, borderRadius: "50%", background: pop, opacity: 0.55 }} />
      <div style={{ position: "relative", marginBottom: 48 }}>
        <Dots index={index} count={count} pop={pop} />
      </div>
      <div style={{ position: "relative", flex: 1, minHeight: 0, display: "flex", flexDirection: "column" }}>
        <Body slide={slide} pop={pop} />
      </div>
      <div style={{ position: "relative", height: 96, marginTop: 40, display: "flex", justifyContent: "flex-end" }}>
        {index < count - 1 && format === "carousel" && <Arrow pop={pop} />}
      </div>
    </AbsoluteFill>
  );
};
