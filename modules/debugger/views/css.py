from ...import ui

line_height = 1.6
header_height = 3
row_height = 3
panel_padding= 2

button = ui.css(padding_left=1, padding_right=1, padding_top=-0.4, padding_bottom=-0.4, background_color='var(--segment-color)', color='var(--primary)', raw='''
	border-radius: 0.4rem;
''')
button_secondary = ui.css(padding_left=1, padding_right=1, padding_top=-0.4, padding_bottom=-0.4, background_color='var(--segment-color)', color='var(--secondary)', raw='''
	border-radius: 0.4rem;
''')

label = ui.css(color='var(--primary)')
label_padding = ui.css(color='var(--primary)')

label_secondary = ui.css(color='var(--secondary)')
label_secondary_padding = ui.css(color='var(--secondary)')

label_redish = ui.css(color='var(--redish)')
label_redish_secondary = ui.css(color='color(var(--redish) alpha(0.7)')

padding = ui.css(padding_left=0.5, padding_right=0.5)
padding_left = ui.css(padding_left=1)

rounded_panel = ui.css(padding_top=1.5, padding_left=1.5, padding_right=1.5, background_color='var(--panel-color)', raw='''
	border-radius: 0.33rem;
''')

tab_panel = ui.css(padding_left=1.5, padding_right=1.5)
tab_panel_selected = ui.css(
	background_color='var(--panel-color)',
	padding_left=1.5,
	padding_right=1.5,
	raw='''
	padding-bottom:2rem;
	border-top-left-radius: 0.33rem;
	border-top-right-radius: 0.33rem;
	'''
)

icon_sized_spacer = ui.css(padding_left=3)
table_inset = ui.css(padding_left=2)

selected = ui.css(background_color='color(var(--accent) alpha(0.2))', raw='border-radius:0.33rem;')
selected_text = ui.css(color='color(var(--accent) alpha(0.75))', padding_left=1, padding_right=1, raw='position: relative; top:-0.2rem;')
