export function upload(selector, options = {}) {
    let files = []
    const input = document.querySelector(selector)
    const preview = document.createElement('div')
    preview.classList.add('preview')

    // создание кнопки с классом и текстом
    const open = document.createElement('button')
    open.classList.add('btn-img')
    open.textContent = 'Открыть'

    if (options.multi){
        input.setAttribute('multiple', true)
    }

    if (options.accept && Array.isArray(options.accept)){
        input.setAttribute('accept', options.accept.join(','))
    }

    input.insertAdjacentElement('afterend', preview)
    input.insertAdjacentElement('afterend', open)

    const triggerInput = () => input.click()
    
    const changeHandler = event => {
        if (!event.target.files.length){
            return
        }
        files = Array.from(event.target.files)


        preview.innerHTML = ''
        // проверка что файл является картинкой
        files.forEach(file => {
            if (!file.type.match('image')){
                return
            }

            const reader = new FileReader()

            reader.onload = ev => {
                const src = ev.target.result
                preview.insertAdjacentHTML('afterbegin', `
                    <div class="preview-img">
                        <div class="preview-remove" data-name="${file.name}">&times;</div>
                        <img src="${src}" alt="${file.name}">
                    </div>
                `)
                // input.insertAdjacentHTML('afterend', `<img src="${ev.target.result}" />`)
            }
            reader.readAsDataURL(file)

        })
    }

    const removeHandler = event => {
        if (!event.target.dataset.name){
            return
        }

        const {name} = event.target.dataset
        files = files.filter(file => file.name !== file.name)

        const block = preview
            .querySelector(`[data-name="${name}"]`)
            .closest('.preview-img')

        block.classList.add('removing')
        setTimeout(() => block.remove(), 300)
    }

    open.addEventListener('click', triggerInput)
    input.addEventListener('change', changeHandler)
    preview.addEventListener('click', removeHandler)

}