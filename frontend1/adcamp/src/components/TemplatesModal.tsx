import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/Dialogue';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/Tabs';

interface TemplatesModalProps {
  isOpen: boolean;
  onClose: () => void;
  templates: {
    [key: string]: string[];
  };
}

export default function TemplatesModal({ 
  isOpen, 
  onClose, 
  templates 
}: TemplatesModalProps) {
  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="max-w-4xl max-h-[80vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle>Optimized Ad Templates</DialogTitle>
        </DialogHeader>
        
        <Tabs defaultValue="awareness" className="w-full">
          <TabsList>
            {Object.keys(templates).map((category) => (
              <TabsTrigger key={category} value={category}>
                {category.charAt(0).toUpperCase() + category.slice(1)}
              </TabsTrigger>
            ))}
          </TabsList>

          {Object.entries(templates).map(([category, templateList]) => (
            <TabsContent key={category} value={category}>
              <div className="space-y-4">
                {templateList.map((template, index) => (
                  <div key={index} className="p-4 border rounded-lg">
                    <p>{template}</p>
                  </div>
                ))}
              </div>
            </TabsContent>
          ))}
        </Tabs>
      </DialogContent>
    </Dialog>
  );
}
