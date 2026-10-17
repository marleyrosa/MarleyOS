'use client';

import Image from 'next/image';
import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Dialog, DialogClose, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog';
import { CoffeeIcon, Heart, QrCodeIcon } from 'lucide-react';

interface DonateDialogProps {
    className?: string;
}

export default function DonateDialog({ className }: DonateDialogProps) {
    const [showQR, setShowQR] = useState(false);

    return (
        <Dialog>
            <DialogTrigger render={<Button variant="outline" className={className} />}>
                <Heart className="w-3 h-3 mr-1.5 text-brand" />
                Donate
            </DialogTrigger>
            <DialogContent className="sm:max-w-md">
                <DialogHeader>
                    <DialogTitle className="flex items-center gap-2">
                        <span>Fuel the Developer</span>
                    </DialogTitle>
                    <DialogDescription className="space-y-2 pt-2">
                        Hi! I&apos;m <strong>Vu</strong>. I&apos;m dedicating my full-time work to building this kit. <br />
                        Your support helps me keep shipping and maintaining it. If you find this tool helpful, please consider buying me a coffee.
                    </DialogDescription>
                </DialogHeader>

                <div className="space-y-3 p-4">
                    {/* Buy Me a Coffee */}
                    <a
                        href="https://buymeacoffee.com/vudovn"
                        target="_blank"
                        rel="noopener noreferrer"
                        className="flex items-center gap-3 p-4 rounded-lg border border-border hover:border-border hover:bg-muted transition-all group"
                    >
                        <div className="flex items-center justify-center w-10 h-10 rounded-full bg-brand/10">
                            <CoffeeIcon className="w-5 h-5 text-brand" />
                        </div>
                        <div className="flex-1">
                            <div className="font-semibold text-foreground mb-0.5">Buy Me a Coffee</div>
                            <div className="text-sm text-muted-foreground">Support via buymeacoffee.com</div>
                        </div>
                        <svg className="w-5 h-5 text-muted-foreground group-hover:text-foreground transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                        </svg>
                    </a>

                    {/* Bank Transfer with QR */}
                    <button
                        onClick={() => setShowQR(!showQR)}
                        className="w-full flex items-center gap-3 p-4 rounded-lg border border-border hover:border-border hover:bg-muted transition-all group text-left"
                    >
                        <div className="flex items-center justify-center w-10 h-10 rounded-full bg-brand/10">
                            <QrCodeIcon className="w-5 h-5 text-brand" />
                        </div>
                        <div className="flex-1">
                            <div className="font-semibold text-foreground mb-0.5">Bank Transfer</div>
                            <div className="text-sm text-muted-foreground">Direct transfer via QR code</div>
                        </div>
                        <svg className={`w-5 h-5 text-muted-foreground transition-transform ${showQR ? 'rotate-90' : ''}`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                        </svg>
                    </button>

                    {/* QR Code Display */}
                    {showQR && (
                        <div className="p-4 rounded-lg border border-border bg-muted/50">
                            <div className="flex flex-col items-center gap-4">
                                {/* QR Code Placeholder - Replace with actual QR code image */}
                                <Image
                                    className="w-48 h-48 rounded-lg"
                                    src="https://img.vietqr.io/image/mbbank-0779440918-compact.jpg"
                                    alt="MB Bank donation QR code"
                                    width={192}
                                    height={192}
                                    unoptimized
                                />
                                {/* Bank Details */}
                                <div className="text-center space-y-1">
                                    <div className="text-sm font-medium text-foreground">
                                        Bank: <span className="font-mono">MB Bank</span>
                                    </div>
                                    <div className="text-sm font-medium text-foreground">
                                        Account: <span className="font-mono">0779440918</span>
                                    </div>
                                    <div className="text-sm font-medium text-foreground">
                                        Name: <span className="font-mono">DO VAN VU</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    )}

                </div>

                <DialogFooter>
                    <DialogClose render={<Button variant="ghost" />}>
                        Close
                    </DialogClose>
                </DialogFooter>
            </DialogContent>
        </Dialog>
    );
}
