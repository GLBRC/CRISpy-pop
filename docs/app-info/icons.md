# Icons

Examples:

- `fa_icon "camera-retro"`
  - `<i class="fa fa-camera-retro"></i>`
- `fa_icon "camera-retro", text: "Take a photo"`
  - `<i class="fa fa-camera-retro"></i> Take a photo`
- `fa_icon "chevron-right", text: "Get started", right: true`
  - `Get started <i class="fa fa-chevron-right"></i>`
- `fa_icon "camera-retro 2x"`
  - `<i class="fa fa-camera-retro fa-2x"></i>`
- `fa_icon ["camera-retro", "4x"]`
  - `<i class="fa fa-camera-retro fa-4x"></i>`
- `fa_icon "spinner spin lg"`
  - `<i class="fa fa-spinner fa-spin fa-lg">`
- `fa_icon "quote-left 4x", class: "pull-left"`
  - `<i class="fa fa-quote-left fa-4x pull-left"></i>`
- `fa_icon "user", data: { id: 123 }`
  - `<i class="fa fa-user" data-id="123"></i>`
- `content_tag(:li, fa_icon("check li", text: "Bulleted list item"))`
  - `<li><i class="fa fa-check fa-li"></i> Bulleted list item</li>`
