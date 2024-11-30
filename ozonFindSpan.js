var all = document.getElementsByTagName("*")
var result = []

for (var i=0, max=all.length; i < max; i++) {
	let nm = all[i]
	let attr = nm.attributes.getNamedItem('class')
	if (attr != null) {
		let el = attr.ownerElement

		style = window.getComputedStyle(el)
		margin = style.getPropertyValue('margin-top')
		textWrap = style.getPropertyValue('text-wrap-mode')
		whiteSpace = style.getPropertyValue('white-space-collapse')
		// console.log(margin, textWrap, whiteSpace)
		
		if (margin == '0px' && textWrap == 'wrap' && whiteSpace == 'preserve-breaks') {
			console.log(el)
			result.push(attr)
		}
	}
}

if (result.length > 0) {
	value = result.at(-1).value
	console.log('requested span element class is', value)
	return value
}

else {
	console.log('no requested spans')
	return null
}

