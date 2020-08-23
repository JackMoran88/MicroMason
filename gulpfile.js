//Подключаем галп
const gulp = require('gulp');
//Объединение файлов
const concat = require('gulp-concat');
//Добапвление префиксов
const autoprefixer = require('gulp-autoprefixer');
//Оптисизация стилей
const cleanCSS = require('gulp-clean-css');
//Оптимизация скриптов
const uglify = require('gulp-uglify');
//Удаление файлов
const del = require('del');
//Синхронизация с браузером
// const browserSync = require('browser-sync').create();
//Для препроцессоров стилей
const sourcemaps = require('gulp-sourcemaps');
//Sass препроцессор
const sass = require('gulp-sass');
//Less препроцессор
// const less = require('gulp-less');
//Stylus препроцессор
// const stylus = require('gulp-stylus');
const imagemin = require('gulp-imagemin');


const styleFilesBootstrap = [
    './static/bootstrap/css/bootstrap.scss'
]
//Порядок подключения файлов со стилями
const styleFiles = [
    './static/src/styles/main.scss',
    './static/src/styles/header.scss',
    './static/src/styles/footer.scss',
    './static/src/styles/card-board.scss',
    './static/src/styles/fonts.scss',
    // './src/css/normalize.scss',
    // './src/css/media.css',
]
//Порядок подключения js файлов
const scriptFiles = [
    // './src/js/lib.js',
    './static/src/js/main.js',
    './static/src/js/ResizeSensor.js',
    // './static/src/js/test.js'
]

//Bootstrap
gulp.task('StyleBootstrap', () => {
    return gulp.src(styleFilesBootstrap)
        .pipe(sourcemaps.init())
        .pipe(sass())
        .pipe(concat('bootstrap.min.css'))
        .pipe(cleanCSS({
            level: 2
        }))
        .pipe(sourcemaps.write('./'))
        //Выходная папка для стилей
        .pipe(gulp.dest('./static/bootstrap/css'))
    // .pipe(browserSync.stream());
});

//Таск для обработки стилей
gulp.task('styles', () => {
    //Шаблон для поиска файлов CSS
    //Всей файлы по шаблону './src/css/**/*.css'
    return gulp.src(styleFiles)
        .pipe(sourcemaps.init())
        //Указать stylus() , sass() или less()
        .pipe(sass())
        //Объединение файлов в один
        .pipe(concat('style.css'))
        //Добавить префиксы
        .pipe(autoprefixer({
            browsers: ['last 2 versions'],
            cascade: false
        }))
        //Минификация CSS
        .pipe(cleanCSS({
            level: 2
        }))
        .pipe(sourcemaps.write('./'))
        //Выходная папка для стилей
        .pipe(gulp.dest('./static/build/styles/'))
    // .pipe(browserSync.stream());
});

//Таск для обработки скриптов
gulp.task('scripts', () => {
    //Шаблон для поиска файлов JS
    //Всей файлы по шаблону './src/js/**/*.js'
    return gulp.src(scriptFiles)
    //Объединение файлов в один
        .pipe(concat('script.js'))
        //Минификация JS
        .pipe(uglify({
            toplevel: true
        }))
        //Выходная папка для скриптов
        .pipe(gulp.dest('./static/build/js'))
    // .pipe(browserSync.stream());
});

//Таск для очистки папки build
gulp.task('del', () => {
    return del(['./static/build/*'])
});

gulp.task('img-compress', () => {
    return gulp.src('./static/src/media/img/**')
        .pipe(imagemin({
            progressive: true
        }))
        .pipe(gulp.dest('./static/build/media/img/'))
});

//Таск для отслеживания изменений в файлах
gulp.task('watch', () => {
    // browserSync.init({
    //    server: {
    //       baseDir: "./"
    //    }
    // });
    // gulp.watch('./static/src/media/img/**', gulp.series('img-compress'));
    //Следить за файлами со стилями с нужным расширением
    gulp.watch('./static/src/styles/**/*.scss', gulp.series('styles'));
    //Следить за JS файлами
    gulp.watch('./static/src/js/**/*.js', gulp.series('scripts'));
    //При изменении HTML запустить синхронизацию
    // gulp.watch("./*.html").on('change', browserSync.reload);
    gulp.watch('./static/bootstrap/css/bootstrap.scss', gulp.series('StyleBootstrap'));
});

//Таск по умолчанию, Запускает del, styles, scripts и watch
gulp.task('default', gulp.series('del', gulp.parallel('styles', 'scripts', 'img-compress', 'StyleBootstrap'), 'watch'));