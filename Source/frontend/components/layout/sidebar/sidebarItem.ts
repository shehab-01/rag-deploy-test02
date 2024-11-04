import {
  ApertureIcon,
  AlertCircleIcon,
  AppWindowIcon,
  BorderAllIcon,
  BoxMultipleIcon,
  CircleIcon,
  CircleFilledIcon,
  CircleDotIcon,
  CopyIcon,
  IconsIcon,
  LayoutGridIcon,
  LayoutDashboardIcon,
  LoginIcon,
  MoodHappyIcon,
  TextSizeIcon,
  TypographyIcon,
  UserPlusIcon,
  AdjustmentsHorizontalIcon
} from 'vue-tabler-icons';

export interface menu {
  header?: string;
  title?: string;
  icon?: any;
  to?: string;
  chip?: string;
  chipColor?: string;
  chipVariant?: string;
  chipIcon?: string;
  children?: menu[];
  disabled?: boolean;
  type?: string;
  subCaption?: string;
}

const sidebarItem: menu[] = [
  {
    header: 'Home',
    children: [
      {
        title: 'Dashboard',
        icon: LayoutDashboardIcon,
        to: '/home/dashboard'
      }
    ]
  },
  {
    header: 'UI',
    children: [
      {
        title: 'Typography',
        icon: TypographyIcon,
        to: '/ui/typography'
      },
      {
        title: 'Shadow',
        icon: CopyIcon,
        to: '/ui/shadow'
      },
      {
        title: 'Alert',
        icon: AlertCircleIcon,
        to: '/ui/alerts'
      },
      {
        title: 'Modal',
        icon: AppWindowIcon,
        to: '/ui/modals'
      },
      {
        title: 'Button',
        icon: CircleDotIcon,
        to: '/ui/buttons'
      },
      {
        title: 'Tab',
        icon: BoxMultipleIcon,
        to: '/ui/tabs'
      },
      {
        title: 'Tables',
        icon: BorderAllIcon,
        to: '/ui/tabels'
      },
      {
        title: 'FormLayout',
        icon: LayoutGridIcon,
        to: '/ui/formlayouts'
      },
      {
        title: 'Curousel',
        icon: AdjustmentsHorizontalIcon,
        to: '/ui/curousel'
      },
      {
        title: 'Icons',
        icon: MoodHappyIcon,
        to: '/ui/icons'
      },
      {
        title: 'Sample Page',
        icon: ApertureIcon,
        to: '/ui/sample-page'
      }
    ]
  },
  {
    header: 'Demo',
    children: [
      {
        title: 'TestFetch',
        icon: CircleIcon,
        to: '/demo/TestFetch'
      },
      {
        title: 'TestCRUD',
        icon: CircleIcon,
        to: '/demo/TestCRUD'
      },
      {
        title: 'Grid1',
        icon: CircleIcon,
        to: '/demo/grid1'
      },
      {
        title: 'Grid2',
        icon: CircleIcon,
        to: '/demo/grid2'
      },
      {
        title: 'CodeInput',
        icon: CircleIcon,
        to: '/demo/CodeInput'
      }
    ]
  },
  {
    header: '공통관리',
    children: [
      {
        title: '코드정보',
        icon: CircleIcon,
        to: '/comm/codelist'
      }
    ]
  },
  {
    header: 'Ai Chat',
    children: [
      {
        title: 'AiChat',
        icon: CircleIcon,
        to: '/ai/AiChat'
      },
      {
        title: 'AiFileUpload',
        icon: CircleIcon,
        to: '/ai/AiFileUpload'
      }
    ]
  },
  {
    header: 'Ai Chat-URL',
    children: [
      {
        title: 'AiChatURL',
        icon: CircleIcon,
        to: '/ai_url/AiChatURL'
      },
      {
        title: 'AiFileUpload',
        icon: CircleIcon,
        to: '/ai/AiFileUpload'
      }
    ]
  }
];

export default sidebarItem;
