const fs = require('fs');
const path = require('path');
const markdownpdf = require('markdown-pdf');

const mdFile = path.join(__dirname, 'technical_documentation.md');
const pdfFile = path.join(__dirname, 'AMC_Chatbot_Documentation.pdf');

const options = {
  remarkable: {
    html: true,
    breaks: true,
    plugins: ['remarkable-meta'],
    syntax: ['footnote', 'sup', 'sub']
  },
  cssPath: path.join(__dirname, 'pdf-style.css')
};

console.log('Converting markdown to PDF...');
markdownpdf(options)
  .from(mdFile)
  .to(pdfFile, function () {
    console.log('PDF generated successfully!');
  }); 