from Algorithms.Halton.Halton import halton
from Algorithms.NBodies.GravityFunctions import repel_cut_gravity
from Algorithms.NBodies.PolyGravityFunctions import side_gravity
from Algorithms.NBodies.RundeKuttaWithPolygonAlgorithm import RungeKuttaWithPolygonAlgorithm
from Front.Utils.Fonts import Fonts
from Front.UiClasses.Frames.AlgorithmFrame import AlgorithmFrame, TextInfo
import customtkinter as ctk
from Front.Utils.MsgBox import MsgBox
from Utils.circle_count import expected_circle_count, expected_circle_count2, expected_circle_count_weighted
import logging

logger = logging.getLogger(__name__)

class QuasiRandomAlgorithmFrame(AlgorithmFrame):
    '''
    Класс для страницы покрытия методом Рунге-Кутты, запущенным
    для квазислучайно расставленных кругов.

    Определяет описание алгоритма, поля заполнения параметров и
    вызов алгоритма с заданными параметрами.
    '''
    title = 'Квазислучайный алгоритм'
    text_info = TextInfo(
        description=
        '''Этот метод пытается оптимизировать покрытие, полученное уравновешиванием системы отталкивающихся друг от друга и от границ многоугольника тел. Круги генерируются квазислучайно равномерно по площади многоугольника с помощью последовательности Халтона (Halton sequence). Затем моделируется поведение системы в заданном промежутке времени.
        ''',
        params=
        '''Этап генерации.
· R - радиус кругов, которыми покрывается многоугольник.
· EXPECTED_CITCLE_COUNT: алгоритм выбирает, какое количество кругов изначально сгенерировать по одной из стратегий:
- Для прямоугольного многоугольника - самая низкая из оценок. Лучше всего подойдёт для многоугольника, имеющего мало скруглений.
- Для круга - самая высокая из оценок. Лучше всего подойдёт для округлых фигур.
- Комбинированная - это копромиссная стратегия. Взвешивает предыдущие две оценки в соотношении 4:1.

· MARGIN - круги генерируются в минимальном описанном для данного многоугольника прямоугольнике. Однако в таком случае круги редко (слишком часто) оказываются у границ. Чтобы исправить это, можно сместить наружу (внутрь) каждую границу описанного прямоугольника на MARGIN.
· P1 - параметр последовательности Халтона для оси x.
· P2 - параметр последовательности Халтона для оси у.
· START - с какого члена последовательности начинать.
· STEP - шаг, с которым брать члены последовательности.

Этап расстановки.
· TIME_START - время, начиная с которого будем моделировать систему.
· TIME_STOP - время, до которого моделируем систему.

· GRAVITY - функция, показывающая степень взаимодействия двух тел. Используется для расчёта передвижения кругов. По сути, задаёт добавку к скорости в данной точке.
· G - константа для масштабирования GRAVITY
· POLY_GRAVITY - функция, показывающая степень взаимодействия тела и многоугольника. По сути, задаёт добавку к скорости в данной точке.
· G_IN_POLY - константа для масштабирования POLY_GRAVITY, если точка лежит внутри многоугольника.
· G_OUTSIDE_POLY - константа для масштабирования POLY_GRAVITY, если точка лежит вне многоугольника.

На больших расстояниях сила притяжения/отталкивания объектов принимается прямо/обратно пропорциональной квадрату расстояния.
· STOP_RADIUS - если два тела (тело и стена) находятся ближе этого расстояния друг от друга, то степень их взаимодействия начинает вычисляться по ограниченной формуле (обратно квадратичная формула даёт очень большой прирост скорости на маленьких расстояниях)
''',
        recommended_values=
        '''· EXPECTED_CIRCLE_COUNT = Комбинированная

· MARGIN = 0 (или другое число из [-R; R])
· P1 = 2
· P2 = 3
P1 и P2 нужно брать взаимно простыми примерно одного порядка (либо пропорционально сторонам многоугольника, если он имеет вытянутую по одной оси форму).
· START = 1 (любое удобное число)
· STEP = 1 (или простое, не равное P1 и P2)

· TIME_START = 0
· TIME_STOP = 50 (между временем моделирования и временем работы линейная зависимость)

· GRAVITY = Ограниченное отталкивание.
· G = 0.2
· POLY_GRAVITY = Затягивающее внутрь.
· G_IN_POLY = 0.15
· G_OUTSIDE_POLY = 10
· STOP_RADIUS = R
''',
        notes=
        '''Это довольно быстрый метод. Он может быстрее остальных покрывать маленькие области, близкие к квадратным. Однако, его покрытия нужно чаще поправлять вручную.
'''
    )

    circle_count_methods = {
        'Для прямоугольного многоугольника': expected_circle_count,
        'Для круга': expected_circle_count2,
        'Комбинированная': expected_circle_count_weighted
    }

    gravities = {
        'Ограниченное отталкивание': repel_cut_gravity,
    }

    poly_gravities = {
        'Затягивающее внутрь': side_gravity,
    }

    def fill_left_panel_(self):
        self.line1 = ctk.CTkFrame(self.left_panel)
        self.line2 = ctk.CTkFrame(self.left_panel)
        self.line3 = ctk.CTkFrame(self.left_panel)
        self.line4 = ctk.CTkFrame(self.left_panel)
        self.line5 = ctk.CTkFrame(self.left_panel)

        # line1 --------------------------------------------------------
        self.alg_label = ctk.CTkLabel(self.line1, text=self.title, font=Fonts.header_font)
        self.alg_label.pack(side='top')
        # line2 --------------------------------------------------------
        self.line2.columnconfigure(0, weight=1)
        self.line2.rowconfigure(0, weight=1)

        self.add_label_input_pair_('R', self.line2, row=0)


        # line3 ---------------------------------------------------------
        self.line3.columnconfigure(0, weight=1)
        self.line3.columnconfigure(1, weight=4)
        self.line3.rowconfigure(tuple(range(6)), weight=1)

        self.add_label_combobox_pair_(
            'EXPECTED_CIRCLE_COUNT',
            self.line3,
            'EXPECTED_CIRCLE_COUNT',
            list(self.circle_count_methods.keys()),
            row=0
        )

        self.add_label_input_pair_('MARGIN', self.line3, row=1)
        self.add_label_input_pair_('P1', self.line3, row=2, type_=int)
        self.add_label_input_pair_('P2', self.line3, row=3, type_=int)
        self.add_label_input_pair_('START', self.line3, row=4, type_=int)
        self.add_label_input_pair_('STEP', self.line3, row=5, type_=int)

        # line4 -----------------------------------------------------------
        self.line4.columnconfigure(0, weight=1)
        self.line4.columnconfigure(1, weight=4)
        self.line4.rowconfigure(tuple(range(2)), weight=1)

        self.add_label_input_pair_('TIME_START', self.line4, row=0, width=50)
        self.add_label_input_pair_('TIME_STOP', self.line4, row=1, width=50)

        # line5 -----------------------------------------------------------
        self.line5.columnconfigure(0, weight=1)
        self.line5.columnconfigure(1, weight=4)
        self.line5.rowconfigure(tuple(range(6)), weight=1)

        self.add_label_combobox_pair_(
            'GRAVITY',
            self.line5,
            'GRAVITY',
            list(self.gravities.keys()),
            row=0
        )
        self.add_label_input_pair_('G', self.line5, row=1)

        self.add_label_combobox_pair_(
            'POLY_GRAVITY',
            self.line5,
            'POLY_GRAVITY',
            list(self.poly_gravities.keys()),
            row=2
        )
        self.add_label_input_pair_('G_IN_POLY', self.line5, row=3)
        self.add_label_input_pair_('G_OUTSIDE_POLY', self.line5, row=4)
        self.add_label_input_pair_('STOP_RADIUS', self.line5, row=5)

        # grid ------------------------------------------------------------
        # Расположим все строки в левой части.

        self.line1.grid(row=0, column=0, stick='news', padx=20, pady=10)
        self.line2.grid(row=1, column=0, stick='news', padx=20, pady=10)
        self.line3.grid(row=2, column=0, stick='news', padx=20, pady=10)
        self.line4.grid(row=3, column=0, stick='news', padx=20, pady=10)
        self.line5.grid(row=4, column=0, stick='news', padx=20, pady=10)



    def run_alg_(self):
        # Получим многоугольник.
        try:
            poly = self.autocad.get_polygons()
        except Exception as e:
            logger.error('Can\'t get polygon from AutoCAD: %s', str(e))
            MsgBox.show_error_msgbox(
                'Не удалось получить многоугольник(и). \nПрервите все активные команды и попробуйте снова.')
            return

        # Получим параметры алгоритма.
        try:
            R = self.get_('R')
            # ---
            exp_circle_cnt_method = self.get_('EXPECTED_CIRCLE_COUNT')
            margin = self.get_('MARGIN')
            p1 = self.get_('P1')
            p2 = self.get_('P2')
            start = self.get_('START')
            step = self.get_('STEP')
            # ---
            time_start = self.get_('TIME_START')
            time_stop = self.get_('TIME_STOP')
            # ---
            gravity = self.get_('GRAVITY')
            g = self.get_('G')

            poly_gravity = self.get_('POLY_GRAVITY')
            g_in_poly = self.get_('G_IN_POLY')
            g_outside_poly = self.get_('G_OUTSIDE_POLY')
            stop_radius = self.get_('STOP_RADIUS')
        except Exception as e:
            logger.error('Can\'t get params for algorithm: %s', str(e))
            MsgBox.show_info_msgbox('Запуск отменён.')
            print('Parsing exception')
            return

        # Запустим алгоритм.
        expected_circles = self.circle_count_methods[exp_circle_cnt_method](poly, R)
        centers = halton(
            P=poly,
            margin=margin,
            n_points=expected_circles,
            p1=p1,
            p2=p2,
            start=start,
            step=step,
        )

        alg = RungeKuttaWithPolygonAlgorithm(poly, centers, R)  # Укажем данные.
        alg.set_params(
            fixed=[0 for _ in range(len(centers))],
            gravity=self.gravities[gravity],
            G=g,
            poly_gravity=self.poly_gravities[poly_gravity],
            poly_G_out=g_outside_poly,
            poly_G_in=g_in_poly,
            STOP_RADIUS=stop_radius,
            TIME_START=time_start,
            TIME_STOP=time_stop
        )  # Укажем параметры решения.

        # Запуск алгоритма
        alg.run_algorithm()  # Запустим алгоритм.
        circles = alg.get_result()  # Получим результат - list[Circle].

        # Вернём ответ.
        try:
            self.autocad.draw_circles(circles)
        except Exception as e:
            logger.debug('Can\'t send circles to AutoCAD: %s', str(e))
            MsgBox.show_error_msgbox(
                'Не удалось отрисовать покрытие. \nПрервите все активные команды и попробуйте снова.')
            return

        logger.info('QuasiRandom algorithm successfully ended.')