(async function autoSavePng() {
    const skeletonList = document.getElementById('skeletonList');
    const loadSkeletonButton = document.getElementById('loadSkeleton');
    const canvas = document.getElementById('canvas');

    // 获取所有选项
    const options = Array.from(skeletonList.options);

    // for (let i = 61; i < options.length; i++) {
    for (let i = 0; i < options.length; i++) {

        const option = options[i];
        // if (parseInt(option.value, 10) < 117131 || parseInt(option.value, 10) > 123031) continue; 

        // 跳过不可用的选项
        if (option.disabled) continue;

        // 选择当前选项
        skeletonList.value = option.value;
        skeletonList.dispatchEvent(new Event('change'));

        // 点击加载按钮
        loadSkeletonButton.click();

        // 等待加载完成
        const loadSuccess = await waitForLoading();

        // 如果加载失败，跳过当前选项
        if (!loadSuccess) {
            console.warn(`选项 "${option.text}" 加载失败，跳过`);
            continue;
        }

        // 保存 canvas 为 PNG
        saveCanvasAsPng(canvas, option.text);
    }

    console.log('所有选项已处理完成！');

    // 等待加载完成的函数
    function waitForLoading() {
        return new Promise((resolve) => {
            const observer = new MutationObserver(() => {
                const loadingText = document.getElementById('loading-text');
                if (loadingText) {
                    const text = loadingText.textContent;

                    // 检查是否加载失败
                    if (text.includes('失败')) {
                        observer.disconnect();
                        resolve(false); // 加载失败
                    } else if (text === '加载完成') {
                        observer.disconnect();
                        // 确保 canvas 渲染完成
                        requestAnimationFrame(() => {
                            resolve(true); // 加载成功
                        });
                    }
                }
            });
            observer.observe(document.body, { childList: true, subtree: true });
        });
    }

    // 保存 canvas 为 PNG 的函数
    function saveCanvasAsPng(canvas, fileName) {
        const link = document.createElement('a');
        link.download = `${fileName}.png`;
        link.href = canvas.toDataURL('image/png');
        link.click();
    }
})();