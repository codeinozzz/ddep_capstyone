#import "common/lib/contentBox.typ": contentBox
#import "common/lib/slideLayouts.typ": theme, mainTitle, layoutA, layoutATwoCols, layoutATwoColsWithTitle, layoutBTwoCols, layoutC, layoutCTwoColsWithTitle, layoutDTwoCols

#mainTitle(
  title: "CSAI-353-Vault",
  subtitle: "Jane Doe <jane.doe@example.com>",
  content: [
    #v(160pt)
    #contentBox(
      fill: luma(150, 30%),
      text(
        fill: white,
        size: 20pt,
        [
          This is a companion document that contains notes and references for the *Deep Learning & Generative AI* course.
        ],
      ),
    )
  ],
)

#layoutC(
  title: "About my project",
  content: [
    #set text(size: 24pt)
    I chose to build a "...", because I want to ...
    #contentBox(
      fill: luma(150, 30%),
      [
        #v(400pt)
      ]
    )
  ],
)
