export interface ModalProps {
  isModalOpen: boolean;
  icon: string;
  title: string;
  description: string;
  maxWidth?: string;
  maxHeight?: string;
  cancelButtonText: string;
  confirmButtonText: string;
}
