// ==UserScript==
// @name         题目爬取脚本
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  爬取题目和答案
// @author       sd0ric4
// @match      	 *://*.chaoxing.com/*
// @grant        none
// ==/UserScript==

(function () {
    'use strict';

    // 获取所有题目的容器
    const questions = document.querySelectorAll('.TiMu');

    // 用于存储所有题目数据的数组
    let data = [];

    questions.forEach((question) => {
        // 获取题目类型
        const type = question.querySelector('.newZy_TItle').innerText.trim().replace(/\n/g, '');

        // 获取题干
        const title = question.querySelector('.font-cxsecret').innerText.trim().replace(/\n/g, '');

        // 获取选项
        let options = [];
        const optionsList = question.querySelectorAll('.Zy_ulTop li');
        optionsList.forEach((option) => {
            options.push(option.innerText.trim().replace(/\n/g, ''));
        });


        // 获取正确答案
        const correctAnswer = question.querySelector('.correctAnswer .answerCon').innerText.trim().replace(/\n/g, '');

        // 将题目数据添加到数组
        data.push({
            type,
            title,
            options,
            correctAnswer
        });
    });

    // 输出JSON格式的数据
    console.log(JSON.stringify(data));

    //下载JSON格式的数据
    const blob = new Blob([JSON.stringify(data)], { type: 'application/json' });
    const a = document.createElement('a');
    a.download = 'data.json';
    a.href = URL.createObjectURL(blob);
})();
